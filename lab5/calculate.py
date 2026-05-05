from task import run_model_with_params
import pprint

node = "node1"
lambda_on_value = 1.0
lambda_off_value = 0.5
lambda_input = 150

result = run_model_with_params(
        node_names=[node],
        lambd=lambda_input,
        fixed_value=None,
        lambda_on=lambda_on_value,
        lambda_off=lambda_off_value
    )

pprint.pprint(result)