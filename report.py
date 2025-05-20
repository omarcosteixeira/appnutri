from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def calcular_imc(peso, altura_cm):
    altura_m = altura_cm / 100
    return peso / (altura_m ** 2)

def classificar_imc(imc):
    if imc < 18.5:
        return "Magreza"
    elif imc <= 24.9:
        return "Peso normal"
    elif imc <= 29.9:
        return "Sobrepeso"
    elif imc <= 39.9:
        return "Obesidade"
    else:
        return "Obesidade grave"

def calcular_rcq(cintura, quadril):
    return cintura / quadril

def calcular_percentual_gordura(sexo, triceps_mm, biceps_mm):
    soma_dobras = triceps_mm + biceps_mm
    if sexo == "masculino":
        percentual = 0.9 * soma_dobras - 0.1
    else:
        percentual = 0.85 * soma_dobras - 0.1
    return max(percentual, 0)

def calcular_tmb(sexo, peso, altura_cm, idade):
    if sexo == "masculino":
        return 66 + (13.7 * peso) + (5 * altura_cm) - (6.8 * idade)
    else:
        return 655 + (9.6 * peso) + (1.8 * altura_cm) - (4.7 * idade)

def calcular_vet(tmb, nivel_atividade):
    fatores = {
        "sedentario": 1.2,
        "leve": 1.375,
        "moderado": 1.55,
        "intenso": 1.725,
    }
    fator = fatores.get(nivel_atividade.lower(), 1.2)
    return tmb * fator

def texto_vet_recomendacao(peso):
    return (
        f"Para manter o peso: 25-35 kcal/kg ({25*peso:.0f}-{35*peso:.0f} kcal)\\n"
        f"Para perder peso: 20-25 kcal/kg ({20*peso:.0f}-{25*peso:.0f} kcal)\\n"
        f"Para ganhar peso: 30-35 kcal/kg ({30*peso:.0f}-{35*peso:.0f} kcal)"
    )

def gerar_relatorio_pdf(dados):
    arquivo = f"relatorio_{datetime.now().strftime('%Y%m%d')}.pdf"
    c = canvas.Canvas(arquivo, pagesize=A4)
    largura, altura = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(largura / 2, altura - 80, "Relatório Nutricional")

    c.setFont("Helvetica", 12)
    y = altura - 120
    linha_espaco = 25

    imc = calcular_imc(dados["peso"], dados["altura"])
    classificacao_imc = classificar_imc(imc)
    rcq = calcular_rcq(dados["cintura"], dados["quadril"])
    percentual_gordura = calcular_percentual_gordura(dados["sexo"], dados["triceps"], dados["biceps"])
    tmb = calcular_tmb(dados["sexo"], dados["peso"], dados["altura"], dados["idade"])
    vet = calcular_vet(tmb, dados["atividade"])

    texto = [
        f"Sexo: {dados['sexo'].capitalize()}",
        f"Idade: {dados['idade']} anos",
        f"Peso: {dados['peso']} kg",
        f"Altura: {dados['altura']} cm",
        f"Cintura: {dados['cintura']} cm",
        f"Quadril: {dados['quadril']} cm",
        f"Dobra Tríceps: {dados['triceps']} mm",
        f"Dobra Bíceps: {dados['biceps']} mm",
        f"Nível de atividade: {dados['atividade'].capitalize()}",
        f"IMC: {imc:.2f} ({classificacao_imc})",
        f"RCQ: {rcq:.2f}",
        f"% Gordura: {percentual_gordura:.2f}%",
        f"TMB: {tmb:.2f} kcal",
        f"VET (Bolso): {vet:.2f} kcal",
        "",
        "Recomendações VET:",
        texto_vet_recomendacao(dados["peso"]),
    ]

    for linha in texto:
        c.drawString(60, y, linha)
        y -= linha_espaco

    data_atual = datetime.now().strftime("%d/%m/%Y")
    c.drawString(60, 60, f"Data do relatório: {data_atual}")

    c.save()
    return arquivo
