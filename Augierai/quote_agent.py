import os
import json
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator

# ==========================================
# 📋 1. Pydantic Data Validation Schemas
# ==========================================

class ShippingItem(BaseModel):
    commodity: str = Field(description="Description of the goods being shipped.")
    weight_kg: float = Field(description="Total weight of the commodity in kilograms.")
    volume_cbm: Optional[float] = Field(None, description="Volume in Cubic Meters.")

    @field_validator("weight_kg")
    @classmethod
    def validate_weight(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Weight must be greater than 0 kg.")
        return v

class QuoteRequest(BaseModel):
    origin: str = Field(description="City or port of departure.")
    destination: str = Field(description="City or port of arrival.")
    container_count: int = Field(default=1, description="Number of containers required.")
    container_type: str = Field(default="20FT Standard", description="Type of container (e.g. 20FT Standard, 40FT High Cube).")
    items: List[ShippingItem] = Field(description="List of cargo commodities included in the shipment.")

    @field_validator("container_count")
    @classmethod
    def validate_containers(cls, v: int) -> int:
        if v < 1:
            raise ValueError("Container count must be at least 1.")
        return v

class FinalQuote(BaseModel):
    request_details: QuoteRequest
    base_rate_usd: float
    handling_fees_usd: float
    total_quote_usd: float
    is_approved: bool
    rejection_reason: Optional[str] = None

# ==========================================
# ⚙️ 2. Core Agentic Workflow Class
# ==========================================

class LogisticsQuoteAgent:
    def __init__(self, use_mock_llm: bool = True):
        self.use_mock_llm = use_mock_llm
        # Simple simulated database for pricing calculations
        self.rate_database = {
            ("karachi", "jebel ali"): {"base": 850.0, "handling": 150.0},
            ("shanghai", "rotterdam"): {"base": 3200.0, "handling": 450.0},
            ("mumbai", "hamburg"): {"base": 2100.0, "handling": 300.0}
        }

    def _call_llm_for_parsing(self, messy_text: str) -> dict:
        """
        Simulates call to Claude/Ollama API with structured JSON output system prompt.
        If using in production, this method calls:
        client.chat.completions.create(model="claude-3-5-sonnet", response_model=QuoteRequest, ...)
        """
        if self.use_mock_llm:
            # Simulated output from LLM parse
            print("[LLM Interface] Simulating LLM extraction...")
            return {
                "origin": "Karachi",
                "destination": "Jebel Ali",
                "container_count": 3,
                "container_type": "40FT High Cube",
                "items": [
                    {"commodity": "Industrial Fan Assemblies", "weight_kg": 8500.0, "volume_cbm": 32.5}
                ]
            }
        else:
            # Example API placeholder
            # import anthropic
            # client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
            raise NotImplementedError("Real API connection requires setting up the client.")

    def calculate_rate(self, request: QuoteRequest) -> FinalQuote:
        """
        Applies logistics rate rules to the validated Pydantic model.
        """
        key = (request.origin.lower().strip(), request.destination.lower().strip())
        
        # Fallback rates if route is not in standard database
        rate_info = self.rate_database.get(key, {"base": 1200.0, "handling": 250.0})
        
        base_rate = rate_info["base"] * request.container_count
        handling_fees = rate_info["handling"]
        total_price = base_rate + handling_fees
        
        # Hard limits check (Business Logic Validation)
        max_weight_limit = 25000.0 # 25 Tons max per container
        total_weight = sum(item.weight_kg for item in request.items)
        
        is_approved = True
        rejection_reason = None
        
        if total_weight > (max_weight_limit * request.container_count):
            is_approved = False
            rejection_reason = "Cargo weight exceeds legal highway safety limits for the requested container count."

        return FinalQuote(
            request_details=request,
            base_rate_usd=base_rate,
            handling_fees_usd=handling_fees,
            total_quote_usd=total_price if is_approved else 0.0,
            is_approved=is_approved,
            rejection_reason=rejection_reason
        )

    def process_shipment_request(self, raw_input: str) -> str:
        """
        Main execution pipeline: raw input -> LLM -> Pydantic -> Business rules -> Output.
        """
        print(f"\n--- Processing New Raw Request ---\nInput:\n{raw_input}\n")
        
        # Step 1: LLM Extraction
        parsed_json = self._call_llm_for_parsing(raw_input)
        
        # Step 2: Pydantic Validation
        try:
            validated_request = QuoteRequest(**parsed_json)
            print("[SUCCESS] Pydantic schema validation passed.")
        except Exception as e:
            return json.dumps({"status": "error", "message": f"Validation failed: {str(e)}"}, indent=2)
            
        # Step 3: Logistics Rate Calculation
        final_quote = self.calculate_rate(validated_request)
        print("[SUCCESS] Pricing calculation and rule checks complete.")
        
        return final_quote.model_dump_json(indent=2)

# ==========================================
# 🧪 3. Run Sample Execution
# ==========================================

if __name__ == "__main__":
    # Sample raw text received via email / messaging
    messy_email = """
    Good morning,
    We need a pricing quote for shipping cargo out from Karachi to Jebel Ali.
    We are moving 3 containers of Industrial Fan Assemblies. The total weight of the goods 
    is 8500 kg, and they take up about 32.5 CBM of volume. We will need the larger 40FT High Cube units.
    Thanks,
    Operational Lead.
    """
    
    agent = LogisticsQuoteAgent(use_mock_llm=True)
    result = agent.process_shipment_request(messy_email)
    print("\nFinal Output JSON:")
    print(result)
