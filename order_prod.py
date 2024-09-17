from dataclasses import dataclass, asdict

@dataclass
class OrdemDeProducao:
    # Atributos Principais
    entrega: str #1 td
    codigo: str #2 td
    cliente: str #3 td
    cod_material: str #4 td
    material: str #5 td
    quantidade: int # 6 td
    nfes: list[int]
    
class OrdensDeProducao:
    # Atributo de classe para armazenar a lista de dicionários
    instances: dict[str, str] = {}

    @classmethod
    def create(cls, entrega: str, codigo: str, cliente: str, cod_material: str, material: str, quantidade: int, nfes: list[int]) -> None:
        # Cria uma nova instância de OP
        instance = OrdemDeProducao(entrega, codigo, cliente, cod_material, material, quantidade, nfes)
        cls.instances[instance.codigo] = asdict(instance)

    @classmethod
    def get_instances(cls) -> "OrdensDeProducao":
        return cls.instances

    @classmethod
    def find_by_codigo(cls, codigo) -> dict[str, str]:
        return cls.instances.get(codigo, None)