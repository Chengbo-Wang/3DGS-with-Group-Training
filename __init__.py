# %%
import torch
from scene.gaussian_model import GaussianModel
from .grouping_method import get_under_training_mask
from arguments import ParamGroup


# %%
class GroupingParams(ParamGroup):
    def __init__(self, parser):
        self.Grouping = True                        # False for Not Plugging in `Group-Training`
        self.grouping_method = 'Opacity-weighted'   # 'Opacity-weighted', 'Random', ...
        self.UTR = 0.6                              # Under Training Ratio
        self.grouping_from_iter = 1000
        self.grouping_until_iter = 29000
        self.grouping_interval = 500                # Control Grouping Frequency
        self.grouping_iteration = [ind_i for ind_i in range(self.grouping_from_iter, self.grouping_until_iter+1, self.grouping_interval)]
        super().__init__(parser, "Grouping Parameters")


# %%
def gaussians_grouping_and_caching(_iteration: int, 
                                   _gaussian_model: GaussianModel, 
                                   _group_training, 
                                   _points_caching=None):
    # Fig 3: Merge Under-Training Group and Caching Group
    if _points_caching != None:  # `_points_caching=None` for the first Grouping iteration / Global training
        _gaussian_model.densification_postfix(**_points_caching)
    # ============================= Grouping =============================
    # Fig 4: No Grouping at iteration I_G/I_O for Global Densify/Optimize
    _UTR = 1.0 if _iteration in [14500, _group_training.grouping_until_iter] else _group_training.UTR
    if _UTR >= 0.999:    # No Grouping for I_D/I_O
        del _points_caching
        assert _gaussian_model.optimizer.param_groups[2]["name"] == "f_rest"
        for param in _gaussian_model.optimizer.param_groups[2]["params"]:
            param.requires_grad = False
        return None
    elif _UTR > 0:      # Grouping
        with torch.no_grad():
            # Fig 3: Sampling
            _mask_under_training = get_under_training_mask(_gaussian_model, _UTR, _group_training.grouping_method)
            _mask_caching = ~_mask_under_training
            # Caching all parameters of Gaussian Model
            # 比如在sort free gs中需要缓存new_features_do和new_features_ro参数
            # For example, it's necessary to cache the `new_features_do` and `new_features_ro` parameters for Sort-free GS (https://arxiv.org/abs/2410.18931).
            """
            _points_caching = {
                "new_xyz": _gaussian_model._xyz[_mask_caching], 
                "new_features_dc": _gaussian_model._features_dc[_mask_caching], 
                "new_features_rest": _gaussian_model._features_rest[_mask_caching], 
                "new_opacities": _gaussian_model._opacity[_mask_caching], 
                "new_scaling" : _gaussian_model._scaling[_mask_caching], 
                "new_rotation" : _gaussian_model._rotation[_mask_caching],
                "new_features_do" : _gaussian_model._features_do[_mask_caching],
                "new_features_ro" : _gaussian_model._features_ro[_mask_caching],
                }
            """
            _points_caching = {
                "new_xyz": _gaussian_model._xyz[_mask_caching], 
                "new_features_dc": _gaussian_model._features_dc[_mask_caching], 
                "new_features_rest": _gaussian_model._features_rest[_mask_caching], 
                "new_opacities": _gaussian_model._opacity[_mask_caching], 
                "new_scaling" : _gaussian_model._scaling[_mask_caching], 
                "new_rotation" : _gaussian_model._rotation[_mask_caching]}

        _gaussian_model.prune_points(_mask_caching)

        return _points_caching
    else:
        ValueError(f"Under-training-ratio {_UTR} is invalid: Must be in (0, 1]")

