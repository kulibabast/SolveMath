from MathTools.combinatorics import solve_combinatorics
from MathTools.polynomial import solve_polynomial
from MathTools.calk import solve_calk

topic_dict = {
    'combinatorics': solve_combinatorics,
    'polynomial': solve_polynomial,
    'calk': solve_calk
}


def solve(request_token: str):
    topic, func_name, request = request_token.split('_')
    answer = topic_dict[topic](func_name, request)
    print(answer)
    return answer


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--q', help='А token on the basis of which mathematical expressions will be derived')
    # args = parser.parse_args()
    # print(args.q)
    # solve(args.q)

    # Testings
    # solve('polynomial_solveLinearEquations_equation=1x-2y~123|2x+3y~12')
    # solve('polynomial_transformationPolynomials_pol1=x^3*y^2+2*x^2*y-3*x*y-6*y;pol2=x*y-2*y;action=div')
    # solve('calk_evalWithNumber_quotient=1*2^2/3*3')
    # solve('polynomial_transformationPolynomials_pol1=x^3*y^2+2*x^2*y-3*x*y-6*y;pol2=x*y-2*y;action=dif')
    # solve('polynomial_transformationPolynomials_pol1=x^3*y^2+2*x^2*y-3*x*y-6*y;pol2=x*y-2*y;action=sum')
    # solve('polynomial_transformationPolynomials_pol1=x^3*y^2+2*x^2*y-3*x*y-6*y;pol2=x*y-2*y;action=expand')
    # solve('polynomial_transformationPolynomials_pol1=x+2;pol2=x+2;action=expand')
    # solve('polynomial_factorPolynomial_pol=x^3-x^2+x-1')
    # solve('calk_primefactorsNumber_n=20')
    # solve('calk_evalWithNumber_quotient=2^2*5^1')
    # solve('calk_getMod_n=3;m=3')
    # solve('calk_roundNumber_n=1.123232;comands=2')
    # solve('polynomial_solveTrigonometric_pol=cosh(x)**2+sinh(x)**2')
    # solve('calk_fact_n=33')
    print('OK')
