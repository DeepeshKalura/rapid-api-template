import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="My API",
    description="API description here - update this for your application",
    version="0.1.0",
    contact={
        "name": "API Support",
        "url": "https://your-website.com",
        "email": "support@your-domain.com",
    },
    terms_of_service="https://your-site.com/terms",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/ping", tags=["Health"])
async def ping():
    return {"status": "ok"}


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Hello World",
        "docs": "/docs",
        "redoc": "/redoc",
    }


ECA_ZONES = [
    {"name": "Baltic Sea", "code": "BALTIC", "fuel_type_required": "VLSFO", "emission_limit": 0.1},
    {
        "name": "North Sea",
        "code": "NORTH_SEA",
        "fuel_type_required": "VLSFO",
        "emission_limit": 0.1,
    },
    {
        "name": "North American ECA",
        "code": "NA_ECA",
        "fuel_type_required": "VLSFO",
        "emission_limit": 0.1,
    },
    {
        "name": "US Caribbean Sea",
        "code": "US_CARIBBEAN",
        "fuel_type_required": "VLSFO",
        "emission_limit": 0.1,
    },
]


# --- Helper Functions ---
def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate great-circle distance between two points."""
    import math

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 3440.1  # Earth's radius in nautical miles
    return c * r


def check_eca_compliance(from_port: str, to_port: str) -> bool:
    """Check if the route passes through ECA zones."""
    eca_ports = ["NLRTM", "DEHAM", "GBLON", "USNYC"]
    return from_port in eca_ports or to_port in eca_ports


# --- Endpoints ---
@app.get("/ping", tags=["Health"])
async def ping():
    """Lightweight health check for serverless/load balancers."""
    return {"status": "ok"}


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "api_version": "0.1.0",
        "service": "eca-marine-api",
    }


@app.get("/ports", response_model=List[Port], tags=["Ports"])
async def list_ports():
    """List all available ports."""
    ports = []
    for code, info in SAMPLE_PORTS.items():
        ports.append(
            Port(
                code=code,
                name=info["name"],
                country=info["country"],
                lat=info["lat"],
                lon=info["lon"],
            )
        )
    return ports


@app.get("/ports/{port_code}", response_model=Port, tags=["Ports"])
async def get_port(port_code: str):
    """Get details for a specific port."""
    port_code = port_code.upper()
    if port_code not in SAMPLE_PORTS:
        raise HTTPException(status_code=404, detail=f"Port {port_code} not found")
    info = SAMPLE_PORTS[port_code]
    return Port(
        code=port_code, name=info["name"], country=info["country"], lat=info["lat"], lon=info["lon"]
    )


@app.get("/eca/zones", response_model=List[ECAZone], tags=["ECA"])
async def list_eca_zones():
    """List all Emission Control Areas."""
    return [ECAZone(**zone) for zone in ECA_ZONES]


@app.post("/routes/calculate", response_model=RouteResponse, tags=["Routes"])
async def calculate_route(request: RouteRequest):
    """Calculate marine route distance and ECA compliance."""
    from_port = request.from_port.upper()
    to_port = request.to_port.upper()

    if from_port not in SAMPLE_PORTS:
        raise HTTPException(status_code=404, detail=f"Origin port {from_port} not found")
    if to_port not in SAMPLE_PORTS:
        raise HTTPException(status_code=404, detail=f"Destination port {to_port} not found")

    origin = SAMPLE_PORTS[from_port]
    destination = SAMPLE_PORTS[to_port]

    distance = haversine_distance(
        origin["lat"], origin["lon"], destination["lat"], destination["lon"]
    )

    eca_compliant = check_eca_compliance(from_port, to_port) if request.eca_compliance else False

    route_type = "ECA Compliant Route" if eca_compliant else "Standard Route"

    return RouteResponse(
        from_port=from_port,
        to_port=to_port,
        distance_nm=round(distance, 2),
        eca_compliance=eca_compliant,
        route_type=route_type,
        estimated_hours=round(distance / 20, 2),  # Assuming average speed of 20 knots
    )


@app.get("/api/info", tags=["Info"])
async def api_info():
    """Get API information and metadata."""
    return {
        "name": "ECA Marine API",
        "version": "0.1.0",
        "description": "API for calculating marine routes, distances, and checking ECA zone compliance",
        "endpoints": [
            {"path": "/ping", "method": "GET", "description": "Health check"},
            {"path": "/ports", "method": "GET", "description": "List all ports"},
            {"path": "/ports/{code}", "method": "GET", "description": "Get port details"},
            {"path": "/eca/zones", "method": "GET", "description": "List ECA zones"},
            {"path": "/routes/calculate", "method": "POST", "description": "Calculate route"},
        ],
    }
