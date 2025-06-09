from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # データベース設定
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "root"  # 本番環境では.envファイルから読み込むべき
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_DATABASE: str = "pos_db"
    
    # SQLAlchemy用のデータベースURL
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

# グローバル設定インスタンス
settings = Settings() 