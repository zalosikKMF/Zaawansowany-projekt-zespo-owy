from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./clearair.db"
    sensor_community_url: str = "https://data.sensor.community"
    sync_country: str = "PL"
    sync_interval_minutes: int = 10
    user_agent: str = "ClearAir/1.0 (projekt edukacyjny; https://github.com/clearair)"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
