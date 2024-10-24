"""
Solicite a matrícula e senha do funcionário para ter acesso aos seus dados.
Solicite o salário base do funcionário.
Pergunte se o funcionário deseja receber vale transporte (s/n).
Pergunte o valor do vale refeição fornecido pela empresa.
Calcule os descontos e acréscimos na folha de pagamento do funcionário.
Mostre o salário líquido do funcionário após os descontos e acréscimos.

Considere que o funcionário possui apenas um dependente.
Considere que o salário base é o salário antes de quaisquer descontos ou acréscimos.
Considere que o salário base, o vale refeição e o plano de saúde são informados em reais (R$).

Alunos: Maria luiza e Henrique Santos 
"""
import os 
os.system("cls || clear")

def calcular_inss(salario):
    if salario <= 1100:
        return salario * 0.075
    elif salario <= 2203.48:
        return salario * 0.09
    elif salario <= 3305.22:
        return salario * 0.12
    elif salario <= 6433.57:
        return salario * 0.14
    else:
        return 854.36
 
def calcular_irrf(salario, dependentes):
    deducao_dependentes = dependentes * 189.59
    base_calculo = salario - deducao_dependentes
    if base_calculo <= 2259.20:
        return 0
    elif base_calculo <= 2826.65:
        return base_calculo * 0.075
    elif base_calculo <= 3751.05:
        return base_calculo * 0.15
    elif base_calculo <= 4664.68:
        return base_calculo * 0.225
    else:
        return base_calculo * 0.275

def calcular_vale_transporte(salario):
    return salario * 0.06

def calcular_vale_refeicao_liquido(valor_vale_refeicao):
  desconto = valor_vale_refeicao * 0.2 
  valor_liquido = valor_vale_refeicao - desconto
  return valor_liquido

def calcular_plano_saude(dependentes):
    return dependentes * 150


matricula = input("Digite sua matrícula: ")
senha = input("Digite sua senha: ")

if matricula == "12345" and senha == "senha123":
    salario_bruto = float(input("Digite seu salário bruto: "))
    dependentes = int(input("Digite a quantidade de dependentes: "))
    vale_transporte = input("Utiliza vale transporte? (s/n): ")
    valor_vale_refeicao = float(input("Digite o valor do vale refeição: "))

    vr = calcular_vale_refeicao_liquido(valor_vale_refeicao)
    inss = calcular_inss(salario_bruto)
    irrf = calcular_irrf(salario_bruto, dependentes)
    vt = calcular_vale_transporte(salario_bruto) if vale_transporte == 's' else 0
    plano_saude = calcular_plano_saude(dependentes)

    descontos = vr + inss + irrf + vt + plano_saude
    salario_liquido = salario_bruto - descontos

    print("\nResumo do pagamento:")
    print(f"Salário Bruto: R$ {salario_bruto:.2f}")
    print(f"Descontos:")
    print(f"  INSS: R$ {inss:.2f}")
    print(f"  IRRF: R$ {irrf:.2f}")
    print(f"  Vale Transporte: R$ {vt:.2f}")
    print(f"  Vale Refeição: R$ {vr:.2f}")
    print(f"  Plano de Saúde: R$ {plano_saude:.2f}")
    print(f"Salário Líquido: R$ {salario_liquido:.2f}")
else:
    print("Autenticação falhou.")