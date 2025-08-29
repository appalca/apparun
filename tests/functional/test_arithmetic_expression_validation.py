import pytest

from apparun.expressions import validate_expr


def test_valid_exprs():
    """
    Check that valid arithmetic expression are seen
    as so.
    """
    exprs = [
        "1",
        "-25",
        "2.486325",
        "-0.158484",
        "15.04e10",
        "78.154984e-10",
        "lifespan",
        "exp(lifespan)",
        "pow(1.0, lifespan)",
        "log(2)",
        "(1.0 * 8 - 9.0e-1 ** cuda_core)",
        "sin(pow(x, y))",
        "log(1.0, exp(-12))",
        "(2 - (x * 8) ** 4.0e9)",
        """12500.0*architecture_Maxwell*(4.6212599075297227e-9*cuda_core
      + 7.37132179656539e-6) + 289.6776199311062*architecture_Maxwell*(0.009702834627645097*cuda_core
      + 1)**2/((1 - 0.6773699850611761*exp(-0.003779619385733156*cuda_core))**2*(70685.775/(0.1889809692866578*cuda_core
      + 19.47688243064738) - 106.7778184271516*sqrt(2)/sqrt(0.009702834627645097*cuda_core
      + 1))) + 12500.0*architecture_Pascal*(4.6891975579761074e-9*cuda_core + 7.808281424221127e-6)
      + 2626.882558417281*architecture_Pascal*(0.0060737847877931227*cuda_core + 1)**2/((1
      - 0.33777635255702983*exp(-0.0065923115776528474*cuda_core))**2*(70685.775/(0.13184623155305694*cuda_core
      + 21.707425626610416) - 101.14318001667067*sqrt(2)/sqrt(0.0060737847877931227*cuda_core
      + 1))) + 0.00036525*energy_per_inference*inference_per_day*lifespan*(0.005*usage_location_EU
      + 0.021*usage_location_FR)""",
        """52.92861728*area**2*defect_density**2*hybrid_bondings/((1
          - exp(-area*defect_density))**2*(70685.775/area - 471.2385*sqrt(2)/sqrt(area)))
          + 1.0*area**2*defect_density**2*three_layers*(1.0*manuf_location_CN*(6764.15753267247/third_layer_node**0.317
          + 42.7549978665) + 1.0*manuf_location_EU*(4095.33859766376/third_layer_node**0.317
          + 59.653139238) + 1.0*manuf_location_FR*(2915.31920449572/third_layer_node**0.317
          + 54.558108576) + 1.0*manuf_location_TW*(6051.14022423897/third_layer_node**0.317
          + 43.2809000325))/((1 - exp(-area*defect_density))**2*(70685.775/area -
          471.2385*sqrt(2)/sqrt(area))) + 123.64492672*area**2*defect_density**2*tsvs/((1
          - exp(-area*defect_density))**2*(70685.775/area - 471.2385*sqrt(2)/sqrt(area)))
          + 1.0*area**2*defect_density**2*(1.0*manuf_location_CN*(6764.15753267247/first_layer_node**0.317
          + 42.7549978665) + 1.0*manuf_location_EU*(4095.33859766376/first_layer_node**0.317
          + 59.653139238) + 1.0*manuf_location_FR*(2915.31920449572/first_layer_node**0.317
          + 54.558108576) + 1.0*manuf_location_TW*(6051.14022423897/first_layer_node**0.317
          + 43.2809000325))/((1 - exp(-area*defect_density))**2*(70685.775/area -
          471.2385*sqrt(2)/sqrt(area))) + 1.0*area**2*defect_density**2*(1.0*manuf_location_CN*(6764.15753267247/second_layer_node**0.317
          + 42.7549978665) + 1.0*manuf_location_EU*(4095.33859766376/second_layer_node**0.317
          + 59.653139238) + 1.0*manuf_location_FR*(2915.31920449572/second_layer_node**0.317
          + 54.558108576) + 1.0*manuf_location_TW*(6051.14022423897/second_layer_node**0.317
          + 43.2809000325))/((1 - exp(-area*defect_density))**2*(70685.775/area -
          471.2385*sqrt(2)/sqrt(area)))""",
    ]

    for expr in exprs:
        if not validate_expr(expr):
            pytest.fail(f"The expression {expr} is valid")


def test_invalid_exprs():
    """
    Check that invalid arithmetic expression are seen
    as so.
    """
    exprs = [
        "with open('file.txt', 'w') as file:\n\tfile.write('this file should not exist')",
        "print('Hello world!')",
        "((1 + 2)",
        ")(1 - 8",
        "1 + + 8",
        "1 - * 5",
        "1 2",
        "exp(1 x 2)",
        "log2(1 x 2)",
        "custom_function(1)",
    ]

    for expr in exprs:
        if validate_expr(expr):
            pytest.fail(f"The expression {expr} is invalid")
