"""
用户服务，处理用户相关的业务逻辑
"""
from src.entity.user import User


class UserService:
    """用户服务类"""
    
    @staticmethod
    def get_user(user_id: int) -> User:
        """
        获取用户信息
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户信息
        """
        # 这里模拟从数据库获取用户信息
        return User(id=user_id, username=f"user{user_id}", email=f"user{user_id}@example.com")
    
    @staticmethod
    def create_user(user: User) -> User:
        """
        创建用户
        
        Args:
            user: 用户信息
            
        Returns:
            创建后的用户信息
        """
        # 这里模拟创建用户并返回，实际应该保存到数据库
        user.id = 1  # 模拟自动生成ID
        return user 