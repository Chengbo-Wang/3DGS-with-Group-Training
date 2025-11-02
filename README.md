
<div align="center">
  <h1 align="center">Faster and Better 3D Splatting via Group Training (ICCV'25)</h1>
  
  <p align="center">
    <a href="https://arxiv.org/pdf/2412.07608" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/badge/Paper-Group_Training" alt="Paper PDF"></a>
    <a href="https://arxiv.org/abs/2412.07608"><img src="https://img.shields.io/badge/arXiv-2412.07608-b31b1b" alt="arXiv"></a>
    <a href="https://chengbo-wang.github.io/3DGS-with-Group-Training/"><img src="https://img.shields.io/badge/Project_Page-green" alt="Project Page"></a>
  </p>

  <p align="center">
    <a href="https://chengbo-wang.github.io/"><strong>Chengbo Wang</strong></a>
    ·
    <a href="https://guozheng-ma.github.io/"><strong>Guozheng Ma</strong></a>
    ·
    <a href="https://github.com/"><strong>Yifei Xue</strong></a>
    ·
    <a href="https://yizhenlao.github.io/"><strong>Yizhen Lao</strong></a>
  </p>

  </div>


This is the repository for the [(ICCV 2025) Faster and Better 3D Splatting via Group Training](https://chengbo-wang.github.io/3DGS-with-Group-Training/).
## 💻Overview

![Overview](./static/images/Method.png)
**Optimizing all Gaussian primitives concurrently during training is not necessary!** Group Training achieves faster reconstruction speeds by training fewer and more important Gaussian primitives, without compromising reconstruction quality. 


## 🚀Quick Start

### 1. Add `Group Trainnig` Repository

***DO NOT*** download the `Group_Training_website` branch, only add the `main` branch.

```shell 
cd <your_3dgs_repo>
# Clone the repository with `-b main --depth 1`
git submodule add -b main --depth 1 https://github.com/Chengbo-Wang/3DGS-with-Group-Training.git ./gaussians_grouping/
git submodule update --init --recursive
```

### 2. Plug in `Group Training` Method

There are 5 places that need to be modified in the `train.py` file.

***Note***: Sometimes it is necessary to initialize/reset certain parameters, such as in LightGaussian and Mip-Splatting as shown in the 3rd modification:

```python
...
#  1st: Import submodule 
from gaussians_grouping import gaussians_grouping_and_caching, GroupingParams
#  2nd: Add two inputs 
def training(..., group_training, point_caching=None):
# ------
  ...
    #  3rd: Grouping before `render()`       
    if group_training.Grouping and iteration in group_training.grouping_iteration:
      # Merge and Grouping
      point_caching = gaussians_grouping_and_caching(iteration, gaussians, group_training, 
                                                      _points_caching=point_caching)
      # ! **Optional**: Initialize `mask_blur` for LightGaussian
      # mask_blur = torch.zeros(gaussians._xyz.shape[0], device='cuda')
      # ! **Optional**: Initialize 3D filter `compute_3D_filter` for Mip-Splatting
      # gaussians.compute_3D_filter(cameras=trainCameras)
    # ------
    render_pkg = render(viewpoint_cam, gaussians, pipe, bg, use_trained_exp=dataset.train_test_exp)
...

if __name__ == "__main__":
  parser = ArgumentParser(description="Training script parameters")
  #  4th: Instantiate `GroupingParams`
  gp = GroupingParams(parser)
  # ------
  ...
  #  5th: Input `group_training` 
  training(..., group_training=gp.extract(args))
  # ------
```

### 3. Optional: Hyperparameters 
- Users can adjust the grouping interval and range of `Class GroupingParams()`
- Or implement a more efficient sampling strategy, please check `get_under_training_mask()` function

### 4. Run
Just run the `full_eval.py` as [3DGS](https://github.com/graphdeco-inria/gaussian-splatting):

```shell
python full_eval.py -m360 <mipnerf360 folder> -tat <tanks and temples folder> -db <deep blending folder>
```

## 🗒️Checklist

- [x] Release the code of `Group Training`
- [ ] More efficient probabilistic sampling method than `torch.multinomial()`


## 📑Citation


If you find `3DGS with Group Training` useful for your work please cite:

```bibtex
@inproceedings{wang2025faster,
  title={Faster and better 3d splatting via group training},
  author={Wang, Chengbo and Ma, Guozheng and Xue, Yifei and Lao, Yizhen},
  booktitle={Proceedings of the IEEE/CVF International Conference on Computer Vision},
  pages={27968--27977},
  year={2025}
}
```
