#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import copy
import traceback
from pathlib import Path
from typing import Any, Dict, List

from classy_vision.generic.registry_utils import import_all_modules


from .constants import ClassyHookFunctions  # isort:skip
from .classy_hook import ClassyHook  # isort:skip


FILE_ROOT = Path(__file__).parent

HOOK_REGISTRY = {}
HOOK_CLASS_NAMES = set()
HOOK_REGISTRY_TB = {}
HOOK_CLASS_NAMES_TB = {}


def register_hook(name, bypass_checks=False):
    """Registers a :class:`ClassyHook` subclass.

    This decorator allows Classy Vision to instantiate a subclass of
    :class:`ClassyHook` from a configuration file, even if the class
    itself is not part of the base Classy Vision framework. To use it,
    apply this decorator to a ClassyHook subclass, like this:

    .. code-block:: python

      @register_hook('custom_hook')
      class CustomHook(ClassyHook):
         ...

    To instantiate a hook from a configuration file, see
    :func:`build_hook`.
    """

    def register_hook_cls(cls):
        if not bypass_checks:
            if name in HOOK_REGISTRY:
                msg = (
                    "Cannot register duplicate hook ({}). Already registered at \n{}\n"
                )
                raise ValueError(msg.format(name, HOOK_REGISTRY_TB[name]))
            if not issubclass(cls, ClassyHook):
                raise ValueError(
                    "Hook ({}: {}) must extend ClassyHook".format(name, cls.__name__)
                )
            if cls.__name__ in HOOK_CLASS_NAMES:
                msg = (
                    "Cannot register hook with duplicate class name({})."
                    + "Previously registered at \n{}\n"
                )
                raise ValueError(
                    msg.format(cls.__name__, HOOK_CLASS_NAMES_TB[cls.__name__])
                )
        tb = "".join(traceback.format_stack())
        HOOK_REGISTRY[name] = cls
        HOOK_CLASS_NAMES.add(cls.__name__)
        HOOK_REGISTRY_TB[name] = tb
        HOOK_CLASS_NAMES_TB[cls.__name__] = tb
        return cls

    return register_hook_cls


def build_hooks(hook_configs: List[Dict[str, Any]]):
    return [build_hook(config) for config in hook_configs]


def build_hook(hook_config: Dict[str, Any]):
    """Builds a ClassyHook from a config.

    This assumes a 'name' key in the config which is used to determine
    what hook class to instantiate. For instance, a config `{"name":
    "my_hook", "foo": "bar"}` will find a class that was registered as
    "my_hook" (see :func:`register_hook`) and call .from_config on
    it."""
    assert hook_config["name"] in HOOK_REGISTRY, (
        "Unregistered hook. Did you make sure to use the register_hook decorator "
        "AND import the hook file before calling this function??"
    )
    hook_config = copy.deepcopy(hook_config)
    hook_name = hook_config.pop("name")
    return HOOK_REGISTRY[hook_name].from_config(hook_config)


# automatically import any Python files in the hooks/ directory
import_all_modules(FILE_ROOT, "classy_vision.hooks")

from .checkpoint_hook import CheckpointHook  # isort:skip
from .torchscript_hook import TorchscriptHook  # isort:skip
from .output_csv_hook import OutputCSVHook  # isort:skip
from .exponential_moving_average_model_hook import (  # isort:skip
    ExponentialMovingAverageModelHook,
)
from .loss_lr_meter_logging_hook import LossLrMeterLoggingHook  # isort:skip
from .model_complexity_hook import ModelComplexityHook  # isort:skip
from .model_tensorboard_hook import ModelTensorboardHook  # isort:skip
from .precise_batch_norm_hook import PreciseBatchNormHook  # isort:skip
from .profiler_hook import ProfilerHook  # isort:skip
from .progress_bar_hook import ProgressBarHook  # isort:skip
from .tensorboard_plot_hook import TensorboardPlotHook  # isort:skip
from .visdom_hook import VisdomHook  # isort:skip


__all__ = [
    "build_hooks",
    "build_hook",
    "register_hook",
    "CheckpointHook",
    "ClassyHook",
    "ClassyHookFunctions",
    "ExponentialMovingAverageModelHook",
    "LossLrMeterLoggingHook",
    "OutputCSVHook",
    "TensorboardPlotHook",
    "TorchscriptHook",
    "ModelComplexityHook",
    "ModelTensorboardHook",
    "PreciseBatchNormHook",
    "ProfilerHook",
    "ProgressBarHook",
    "VisdomHook",
]
