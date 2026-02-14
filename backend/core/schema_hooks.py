"""
Hooks para configuração personalizada do drf-spectacular.
Remove tags automáticas 'v1' geradas do prefixo da URL.
"""


def postprocessing_filter_spec(result, generator, request, public):
    """
    Remove tags automáticas 'v1' geradas pelo framework.
    Garante que apenas tags definidas manualmente apareçam no Swagger.
    
    Args:
        result: Dict contendo os componentes do schema OpenAPI
        generator: Generator instance
        request: HTTPRequest
        public: Boolean indicando se é público
        
    Returns:
        Dict com o schema processado
    """
    if 'tags' in result:
        result['tags'] = [
            tag for tag in result['tags'] 
            if tag.get('name') != 'v1'
        ]
    
    if 'paths' in result:
        for path, methods in result['paths'].items():
            if isinstance(methods, dict):
                for method, operation in methods.items():
                    if isinstance(operation, dict) and 'tags' in operation:
                        operation['tags'] = [
                            tag for tag in operation['tags'] 
                            if tag != 'v1'
                        ]
    
    return result

