import logging
import sys

from pydantic_core import ValidationError

logger = logging.getLogger(__name__)


def init_logger():
    """
    Init the logger so that all the logs are saved
    in a file named apparun.log and are redirected on
    the standard output.
    """
    logger.setLevel(level=logging.DEBUG)

    # Format the message in the logs
    formatter = logging.Formatter(
        "{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
    )

    # Write the logs in a file
    file_handler = logging.FileHandler("apparun.log", mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Redirect all the logs to stdout
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)


def log_exprs_error(error: ValidationError):
    for err in error.errors():
        match err["type"]:
            case "float_expr":
                logger.error(
                    "Invalid float type expression for the parameter %s: %s",
                    err["ctx"]["target_parameter"],
                    err["input"],
                )
            case "no_such_param":
                for param in err["ctx"]["invalid_parameters"]:
                    logger.error("No such parameter: %s", param)
            case "dependencies_type":
                logger.error(
                    "The dependencies %s have an invalid type for the expression %s, expected type %s",
                    "(" + ", ".join(err["ctx"]["invalid_parameters"]) + ")",
                    err["input"],
                    err["ctx"]["required_type"],
                )
            case "too_much_dependencies":
                logger.error(
                    "Too much dependencies for the expression %s, expected %s but got %s",
                    err["input"],
                    err["ctx"]["required"],
                    err["ctx"]["value"],
                )
            case "enum_expr_empty_options":
                logger.error(
                    "The options for the enum type expression %s, don't have an associated sub expression: %s",
                    err["input"],
                    ", ".join(err["ctx"]["invalid_options"]),
                )
            case "enum_expr_options":
                if err["ctx"]["missing_options"]:
                    logger.error(
                        "Missing options for the enum type expression %s: %s",
                        err["input"],
                        ", ".join(err["ctx"]["missing_options"]),
                    )
                else:
                    logger.error(
                        "Non possible options for the enum type expression %s: %s",
                        err["input"],
                        ", ".join(err["ctx"]["extra_options"]),
                    )
            case "empty_list":
                logger.error(
                    "Lists values for parameters can't be empty lists, but the parameter %s has one",
                    err["ctx"]["parameter"],
                )
            case "lists_size_match":
                logger.error("Lists values must have matching size")
            case "dependencies_cycle":
                logger.error(
                    "The values for the parameters %s are inter-dependent",
                    "(" + ", ".join(err["ctx"]["parameters"]) + ")",
                )
            case "value_error":
                if err["input"] is not None:
                    logger.error(
                        "Invalid value %s for the parameter %s, got after evaluating the expression %s",
                        err["ctx"]["value"],
                        err["ctx"]["target_parameter"],
                        err["input"],
                    )
                else:
                    logger.error(
                        "Invalid value %s for the parameter %s",
                        err["ctx"]["value"],
                        err["ctx"]["target_parameter"],
                    )
