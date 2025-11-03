# input_validators.py - Validadores de entrada en tiempo real
class InputValidators:
    @staticmethod
    def validate_states(value):
        """Valida entrada de estados: solo letras y comas"""
        if not value:
            return True
        for char in value:
            if not (char.isalpha() or char == ','):
                return False
        return True
    
    @staticmethod
    def validate_symbols(value):
        """Valida entrada de símbolos: exactamente 2 números separados por coma"""
        if not value:
            return True
        
        # Solo permite números (0-9) y comas
        for char in value:
            if not (char.isdigit() or char == ','):
                return False
        
        # Contar comas - máximo 1 coma
        commas = value.count(',')
        if commas > 1:
            return False
        
        # No permitir comas dobles
        if ',,' in value:
            return False
        
        # No permitir que empiece con coma
        if value.startswith(','):
            return False
        
        return True
    
    @staticmethod
    def validate_initial_state(value):
        """Valida estado inicial: solo una letra"""
        if not value:
            return True
        return len(value) == 1 and value.isalpha()
    
    @staticmethod
    def validate_final_states(value):
        """Valida estados finales: solo letras y comas"""
        if not value:
            return True
        for char in value:
            if not (char.isalpha() or char == ','):
                return False
        return True
    
    @staticmethod
    def validate_matrix_cell(value):
        """Valida celdas de matriz: solo letras y comas para múltiples destinos"""
        if not value:
            return True
        for char in value:
            if not (char.isalpha() or char == ','):
                return False
        return True
    
    @staticmethod
    def validate_binary(value):
        """Valida campos binarios: solo 0 o 1"""
        if not value:
            return True
        return len(value) == 1 and value in ['0', '1']