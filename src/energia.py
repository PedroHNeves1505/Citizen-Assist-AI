TARIFA_KWH = 0.85          
FATOR_CO2 = 0.085          
REDUCAO_EFICIENCIA = 0.18  
REDUCAO_SOLAR = 0.85       
INVESTIMENTO_EFICIENCIA = 150.00
INVESTIMENTO_SOLAR = 9500.00

def calcular_conta(consumo_kwh: float) -> float:
    """Retorna o valor estimado da conta de luz em R$."""
    return consumo_kwh * TARIFA_KWH

def classificar_consumo(consumo_kwh: float) -> str:
    """Classifica o consumo mensal no padrão do semáforo (Verde/Amarelo/Vermelho)."""
    if consumo_kwh <= 180:
        return "VERDE"
    elif consumo_kwh <= 350:
        return "AMARELO"
    else:
        return "VERMELHO"

def recomendar(consumo_kwh: float) -> str:
    """Retorna uma recomendação textual personalizada."""
    faixa = classificar_consumo(consumo_kwh)
    conta = calcular_conta(consumo_kwh)
    
    if faixa == "VERDE":
        return (f"Seu consumo é baixo ({consumo_kwh:.1f} kWh/mês, ~R$ {conta:.2f}). "
                "Continue com bons hábitos! Considere lâmpadas LED para economizar ainda mais.")
    elif faixa == "AMARELO":
        return (f"Seu consumo é moderado ({consumo_kwh:.1f} kWh/mês, ~R$ {conta:.2f}). "
                "Evite usar ar-condicionado e chuveiro elétrico no horário de pico (18h-21h). "
                "Uma opção é investir em eficiência energética (payback ~7 meses).")
    else:  # VERMELHO
        return (f"Seu consumo é alto ({consumo_kwh:.1f} kWh/mês, ~R$ {conta:.2f}). "
                "Priorize a limpeza de filtros de ar-condicionado e evite aparelhos pesados no pico. "
                "Considere energia solar compartilhada por assinatura (sem obras).")

def calcular_economia(consumo_kwh: float) -> dict:
    """Retorna um dicionário com economia estimada para cada alternativa."""
    conta_atual = calcular_conta(consumo_kwh)
    
    consumo_eficiente = consumo_kwh * (1 - REDUCAO_EFICIENCIA)
    economia_eficiencia = conta_atual - calcular_conta(consumo_eficiente)
    payback_eficiencia = INVESTIMENTO_EFICIENCIA / economia_eficiencia if economia_eficiencia > 0 else 0
    
    consumo_solar = consumo_kwh * (1 - REDUCAO_SOLAR)
    economia_solar = conta_atual - calcular_conta(consumo_solar)
    payback_solar = INVESTIMENTO_SOLAR / economia_solar if economia_solar > 0 else 0
    
    co2_evitado_solar = (consumo_kwh - consumo_solar) * FATOR_CO2
    
    return {
        "eficiencia": {
            "economia_mensal": economia_eficiencia,
            "payback_meses": payback_eficiencia,
            "investimento": INVESTIMENTO_EFICIENCIA
        },
        "solar": {
            "economia_mensal": economia_solar,
            "payback_meses": payback_solar,
            "investimento": INVESTIMENTO_SOLAR,
            "co2_evitado_kg": co2_evitado_solar
        }
    }