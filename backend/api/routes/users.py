from fastapi import APIRouter

# TODO: Implement user profile endpoints
# - GET /api/users/me  (requires auth)
# - PUT /api/users/me  (update profile)

router = APIRouter()


@router.get("/me")
def get_me():
    return {"message": "User profile endpoint - not yet implemented", "success": False}
