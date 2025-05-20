from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def calcular_resultados(dados):
    peso = dados["peso"]
    altura_cm = dados["altura"]
    altura_m = altura_cm / 100
    cintura = dados["cintura"]
    quadril = dados["quadril"]
    idade = dados["idade"]
    sexo = dados["sexo"]
    triceps = dados["triceps"]
    biceps = dados["biceps"]

    # IMC
    imc = peso / (altura_m ** 2)

    # RCQ
    rcq = cintura / quadril

    # Soma das dobras
    S = triceps + biceps

    # Densidade corporal (Pollock simplificado para 2 dobras)
    if sexo == "masculino":
        densidade = 1.097 - (0.000815 * S) + (0.00000084 * S**2) - (0.0002574 * idade)
    else:
        densidade = 1.089733 - (0.0009245 * S) + (0.0000025 * S**2) - (0.0000979 * idade)

    # % de Gordura (Fórmula de Siri)
    perc_gordura = ((4.95 / densidade) - 4.5) * 100

    # TMB (Harris-Benedict)
    if sexo == "masculino":
        tmb = 88.36 + (13.4 * peso) + (4.8 * altura_cm) - (5.7 * idade)
    else:
        tmb = 447.6 + (9.2 * peso) + (3.1 * altura_cm) - (4.3 * idade)

    # Fator atividade
    fatores = {
        "sedentario": 1.2,
        "leve": 1.375,
        "moderado": 1.55,
        "intenso": 1.725
    }
    fator = fatores.get(dados["atividade"], 1.2)
    vet = tmb * fator

    return {
        "IMC": round(imc, 2),
        "RCQ": round(rcq, 2),
        "% Gordura": round(perc_gordura, 2),
        "TMB": round(tmb),
        "VET": round(vet)
    }

def gerar_relatorio_pdf(dados):
    resultados = calcular_resultados(dados)
    data_hoje = datetime.now().strftime("%d/%m/%Y")

    nome_pdf = f"relatorio_{data_hoje.replace('/', '-')}.pdf"
    c = canvas.Canvas(nome_pdf, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "📋 Relatório de Avaliação Nutricional")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Data: {data_hoje}")
    c.drawString(50, height - 110, f"Sexo: {dados['sexo'].capitalize()}")
    c.drawString(50, height - 130, f"Idade: {dados['idade']} anos")
    c.drawString(50, height - 150, f"Peso: {dados['peso']} kg")
    c.drawString(50, height - 170, f"Altura: {dados['altura']} cm")
    c.drawString(50, height - 190, f"Cintura: {dados['cintura']} cm")
    c.drawString(50, height - 210, f"Quadril: {dados['quadril']} cm")
    c.drawString(50, height - 230, f"Tríceps: {dados['triceps']} mm")
    c.drawString(50, height - 250, f"Bíceps: {dados['biceps']} mm")
    c.drawString(50, height - 270, f"Atividade: {dados['atividade'].capitalize()}")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 310, "📊 Resultados:")

    c.setFont("Helvetica", 12)
    y = height - 340
    for chave, valor in resultados.items():
        c.drawString(60, y, f"{chave}: {valor}")
        y -= 20

    c.save()
    return nome_pdf
