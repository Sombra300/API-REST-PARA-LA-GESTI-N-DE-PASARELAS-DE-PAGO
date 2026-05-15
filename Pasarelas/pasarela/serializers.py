from rest_framework import serializers
from .models import Provider, Transaction, Incidence

# SERIALIZER DE PROVEEDORES
class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Provider
        fields='__all__'
    
        # Validar name
    def validate_name(self, value):

        if value is None or value.strip()=='':
            raise serializers.ValidationError('El nombre no puede estar vacío')

        if len(value)>100:
            raise serializers.ValidationError('El nombre es demasiado largo')

        return value
    
    # Validar api_key
    def validate_api_key(self, value):

        if value is None or value.strip()=='':
            raise serializers.ValidationError('La API Key no puede estar vacía')

        return value
    

    # Validar environment
    def validate_environment(self, value):

        valid_options=['dev', 'test', 'prod']

        if value not in valid_options:
            raise serializers.ValidationError('Opción de entorno no válida')

        return value


# SERIALIZER DE TRANSACCIONES
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transaction
        fields='__all__'

    # Validar amount
    def validate_amount(self, value):

        if value is None:
            raise serializers.ValidationError('Debes indicar un importe')

        if value==0:
            raise serializers.ValidationError('El importe debe tener un valor')

        return value
    
    # Validar currency
    def validate_currency(self, value):

        if any(char.isdigit() for char in value):
            raise serializers.ValidationError('La moneda no puede contener números')

        if len(value)>10:
            raise serializers.ValidationError('La moneda supera el tamaño máximo')

        return value
    
    # Validar payment_state
    def validate_payment_state(self, value):

        valid_options=[
            'pending',
            'completed',
            'failed',
            'refunded'
        ]

        if value not in valid_options:
            raise serializers.ValidationError('Estado de pago no válido')

        return value
    
    # Validación general
    def validate(self, data):

        provider=data.get('id_proveedor')

        if provider is None:
            raise serializers.ValidationError('Datos del proveedor no encontrados para la transaccion')

        return data



# SERIALIZER DE INCIDENCIAS
class IncidenceSerializer(serializers.ModelSerializer):

    class Meta:
        model=Incidence
        fields='__all__'

    # Validar description
    def validate_description(self, value):

        if len(value)>500:
            raise serializers.ValidationError('La descripción es demasiado larga')

        return value

    # Validar type
    def validate_type(self, value):

        valid_options=[
            'nonpayment',
            'connection_error',
            'devolution',
            'timeout',
            'authentication_error'
        ]

        if value not in valid_options:
            raise serializers.ValidationError('Tipo de incidencia no válido')

        return value

    # Validación general
    def validate(self, data):

        transaction=data.get('id_transaction')

        if transaction is None:
            raise serializers.ValidationError('Datos de la transaccion no encontrados para la transaccion')

        return data