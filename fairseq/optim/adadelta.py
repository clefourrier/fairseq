# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree. An additional grant of patent rights
# can be found in the PATENTS file in the same directory.

import torch.optim

from . import FairseqOptimizer, register_optimizer


@register_optimizer('adadelta')
class Adadelta(FairseqOptimizer):
    def __init__(self, args, params):
        super().__init__(args, params)
        self._optimizer = torch.optim.Adadelta(params, **self.optimizer_config)

    @staticmethod
    def add_args(parser):
        """Add optimizer-specific arguments to the parser."""
        parser.add_argument('--adadelta-rho', type=float, default=0.9, metavar='RHO',
                            help='coefficient used for computing a running average of squared gradients')
        parser.add_argument('--adadelta-eps', type=float, default=1e-6, metavar='EPS',
                            help='term added to the denominator to improve numerical stability')

    @property
    def optimizer_config(self):
        """
        Return a kwarg dictionary that will be used to override optimizer
        args stored in checkpoints. This allows us to load a checkpoint and
        resume training using a different set of optimizer args, e.g., with a
        different learning rate.
        """
        return {
            'lr': self.args.lr[0],
            'rho': self.args.adadelta_rho,
            'eps': self.args.adadelta_eps,
            'weight_decay': self.args.weight_decay,
        }