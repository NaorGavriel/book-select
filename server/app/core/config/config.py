import os
from .settings import Settings
from .aws_loader import load_ssm_parameters


def get_settings():

    deployment = os.getenv("DEPLOYMENT_TYPE", "local")

    if deployment == "aws":

        region = os.environ["AWS_REGION"]

        aws_params = load_ssm_parameters(region)

        return Settings(**aws_params)

    return Settings()


settings = get_settings()