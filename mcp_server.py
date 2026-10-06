"""
Agri-Vincent AI - MCP Server
Climate-smart maize farming tools.

Prototype MCP implementation for:
- maize planting
- fertilizer management
- pest and disease management
- climate-smart farming
- harvest and storage
- market planning
"""

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Agri-Vincent AI")


@mcp.tool()
def maize_planting_advice(
    location: str = "Rwanda",
    season: str = "current season",
    soil_condition: str = "unknown",
) -> str:
    """Provide practical, climate-smart maize planting guidance."""

    return f"""
Agri-Vincent AI – Maize Planting Advice

Location: {location}
Season: {season}
Soil condition: {soil_condition}

Recommended actions:
1. Prepare the field early and improve soil structure.
2. Use certified, good-quality maize seed suited to the local environment.
3. Plant when soil moisture is adequate and rainfall is reasonably established.
4. Avoid planting in waterlogged soil.
5. Use appropriate spacing recommended for the selected maize variety.
6. Apply organic matter where available to improve soil health.
7. Monitor rainfall and crop emergence after planting.

Important:
Exact planting dates and fertilizer rates should be adjusted using
local agricultural recommendations, soil information and current weather data.
"""


@mcp.tool()
def fertilizer_advice(
    crop_stage: str = "early growth",
    soil_condition: str = "unknown",
) -> str:
    """Provide maize fertilizer management guidance."""

    return f"""
Agri-Vincent AI – Fertilizer Advice

Crop stage: {crop_stage}
Soil condition: {soil_condition}

Guidance:
1. Base fertilizer decisions on soil condition and crop requirements.
2. Apply fertilizer at the appropriate crop growth stage.
3. Place fertilizer correctly so that it is available to the maize roots.
4. Avoid applying fertilizer immediately before heavy rainfall.
5. Do not over-apply fertilizer because it can increase costs and cause nutrient losses.
6. Combine mineral fertilizers with organic matter where appropriate.
7. Follow local extension-service recommendations for exact rates.

For an exact fertilizer recommendation, soil-test information,
maize variety, field size and local agricultural guidance should be considered.
"""


@mcp.tool()
def pest_disease_advice(
    symptoms: str = "unknown",
) -> str:
    """Provide integrated pest and disease management guidance for maize."""

    return f"""
Agri-Vincent AI – Pest and Disease Advice

Observed symptoms: {symptoms}

Recommended approach:
1. Inspect the whole field regularly.
2. Check leaves, stems, roots and maize ears for unusual symptoms.
3. Identify the pest or disease before selecting a control method.
4. Remove or manage heavily affected plants when appropriate.
5. Maintain field sanitation and control weeds.
6. Use healthy and quality seed.
7. Encourage integrated pest management rather than relying only on pesticides.
8. If pesticide treatment is necessary, use only an officially recommended
   product and follow its label, safety instructions and local agricultural advice.

If the symptoms are unclear, consult a qualified agricultural extension officer
before applying chemicals.
"""


@mcp.tool()
def climate_smart_maize_advice(
    weather_risk: str = "variable rainfall",
) -> str:
    """Provide climate-smart maize farming recommendations."""

    return f"""
Agri-Vincent AI – Climate-Smart Maize Advice

Current weather risk: {weather_risk}

Recommended practices:
1. Monitor reliable weather forecasts before major field operations.
2. Time planting around suitable soil moisture and rainfall.
3. Use drought-tolerant or locally recommended varieties when appropriate.
4. Improve soil organic matter and soil-water retention.
5. Reduce unnecessary soil disturbance where suitable.
6. Use mulching or other moisture-conservation practices where appropriate.
7. Diversify farm practices to reduce climate-related production risks.
8. Keep records of rainfall, planting dates, fertilizer use and yields.

Climate-smart farming should combine productivity, soil health,
water management and resilience to climate variability.
"""


@mcp.tool()
def harvest_storage_advice(
    grain_condition: str = "mature",
) -> str:
    """Provide maize harvesting and storage guidance."""

    return f"""
Agri-Vincent AI – Harvest and Storage Advice

Grain condition: {grain_condition}

Guidance:
1. Harvest when maize is physiologically mature and sufficiently dry for the
   intended storage system.
2. Avoid harvesting during wet conditions where possible.
3. Dry maize properly before long-term storage.
4. Remove damaged, mouldy or visibly contaminated grain.
5. Store maize in a clean, dry and well-managed storage facility.
6. Protect stored grain from insects, rodents, moisture and contamination.
7. Inspect stored maize regularly.
8. Use safe, locally recommended grain-protection practices.

Good post-harvest management helps reduce losses and protects food quality.
"""


@mcp.tool()
def maize_market_planning(
    quantity_kg: float = 0,
    need_to_sell_immediately: bool = False,
) -> str:
    """Provide maize market planning guidance."""

    return f"""
Agri-Vincent AI – Maize Market Planning

Quantity: {quantity_kg} kg
Immediate sale needed: {need_to_sell_immediately}

Recommended actions:
1. Identify potential buyers before harvest.
2. Compare prices from different legitimate market channels.
3. Consider transport, storage and transaction costs before accepting a price.
4. Grade and maintain maize quality to improve market opportunities.
5. Avoid distress selling when safe storage and cash-flow conditions allow.
6. Keep records of quantities, prices, buyers and transaction costs.
7. Explore farmer groups or aggregation opportunities where available.

Current market prices should come from a verified and up-to-date market data source.
This prototype does not claim to provide live market prices.
"""


@mcp.tool()
def farm_decision_support(
    farm_size_ha: float,
    crop_stage: str,
    main_problem: str,
) -> str:
    """Combine basic farm information into a practical decision-support checklist."""

    return f"""
Agri-Vincent AI – Farm Decision Support

Farm size: {farm_size_ha} hectares
Crop stage: {crop_stage}
Main problem: {main_problem}

Decision checklist:
1. Identify the main production problem.
2. Check soil moisture and recent weather conditions.
3. Inspect the crop for pests, diseases and nutrient deficiencies.
4. Review recent fertilizer and field-management activities.
5. Consider the cost and expected benefit of each intervention.
6. Use locally recommended agricultural practices.
7. Monitor the result after taking action.
8. Escalate uncertain or serious cases to an agricultural extension professional.

Human-in-the-loop:
The AI provides decision support. The farmer or qualified agricultural
professional remains responsible for the final farm decision.
"""

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
        stateless_http=True,
        json_response=True,
    )
