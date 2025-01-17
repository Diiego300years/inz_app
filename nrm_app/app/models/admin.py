from flask_login import UserMixin
import datetime
from app import db, bcrypt
import uuid
from sqlalchemy.dialects.postgresql import UUID
from flask_jwt_extended import create_access_token, decode_token
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


class AdminModel(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(64), nullable=False, index=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    added_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    confirmed = db.Column(db.Boolean, default=False, nullable=False)
    is_account_active =  db.Column(db.Boolean, default=True, nullable=False)

    @property
    def password(self):
        raise AttributeError('Password is write-only')

    @property
    def is_active(self):
        """
        Flask-Login expects this method to check if the user account is active.
        Typically, you might check if the user has confirmed their account.
        """
        return self.is_account_active

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


    def generate_confirmation_token(self, expiration=3600):
        """
        Generuje token JWT do potwierdzenia konta z czasem ważności (domyślnie 1 godzina).

        :param expiration: Czas ważności tokenu w sekundach (domyślnie 3600 sekund)
        :return: Zwraca zakodowany token jako string
        """
        expires_delta = datetime.timedelta(seconds=expiration)

        token = create_access_token(identity=self.id, expires_delta=expires_delta)


        return token

    def confirm_token(self, token):
        """
        Weryfikuje i dekoduje token JWT.

        :param token: JWT Token to verify
        :return: True, if token is correct, False in other case
        """
        try:
            payload = decode_token(token)  # Dekodowanie tokenu
        except ExpiredSignatureError:
            print("Token expired.")
            return False
        except InvalidTokenError:
            print("Invalid token.")
            return False
        except Exception as e:
            print("sthis happended: ", e)
            return False

        # Read identity from sub (default place for holding identity from method create_access_token )
        if str(payload.get('sub')) != str(self.id):
            print("Token doesn't match user ID")
            return False

        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return (f'User(name={self.name},'
                f'email={self.email},'
                f'added_at={self.added_at},'
                f'confirmed={self.confirmed},'
                f'is_account_active={self.is_account_active})')
