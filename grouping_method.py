# %%
import torch
from scene import GaussianModel

# %%
def get_under_training_mask(_gaussian_model: GaussianModel, under_training_ratio, grouping_method='Random'):
    _num_gaussian = _gaussian_model._xyz.shape[0]
    if grouping_method == 'Random':
        _ind_UT = torch.rand([_num_gaussian, ]) < under_training_ratio
    elif grouping_method == 'Volume-weighted':
        _theta_all = torch.prod(_gaussian_model.get_scaling, dim=-1).squeeze(-1)    # torch.Tensor([num_gaussians, 3]) > prod > torch.Tensor([num_gaussians, 1])
        _prob_UT = _theta_all / torch.sum(_theta_all)                               # Opacity-weighted probability
        _ind_UT = torch.multinomial(_prob_UT, 
                                    int(_num_gaussian * under_training_ratio), 
                                    replacement=False)
    elif grouping_method == 'Opacity-weighted':
        _theta_all = _gaussian_model.get_opacity.squeeze(-1)
        _prob_UT = _theta_all / torch.sum(_theta_all)
        _ind_UT = torch.multinomial(_prob_UT, 
                                    int(_num_gaussian * under_training_ratio), 
                                    replacement=False)
    elif grouping_method == 'Opacity-Volume-weighted':
        _theta_all = _gaussian_model.get_opacity.squeeze(-1)
        _theta_all *= torch.prod(_gaussian_model.get_scaling, dim=-1).squeeze(-1)
        _prob_UT = _theta_all / torch.sum(_theta_all)
        _ind_UT = torch.multinomial(_prob_UT, 
                                    int(_num_gaussian * under_training_ratio), 
                                    replacement=False)
    else:
        raise NotImplementedError
    
    _mask_under_training = torch.zeros(_num_gaussian, dtype=torch.bool)
    _mask_under_training[_ind_UT] = True        # Under-training mask, Ture means under-training

    return _mask_under_training
