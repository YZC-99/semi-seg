from torchvision.models import resnet18,resnet50
import segmentation_models_pytorch as smp
import torchvision.models.segmentation as seg
from torchcam.methods import GradCAMpp
from torchcam.utils import overlay_mask
from torchvision.io.image import read_image
from torchvision.transforms.functional import normalize, resize, to_pil_image
import matplotlib.pyplot as plt
import torch

def hook(module, input, output):
    # 在这里对输入或输出进行处理，这里以输出为例
    print("Layer输出:", output.shape)

# 定义模型
model = resnet50(pretrained=True).eval()
# num_ftrs = model.fc.in_features
# model.fc = torch.nn.Linear(num_ftrs, 2)
# model = smp.Unet(classes=2).eval()
# print(model)
# layer4 = model.segmentation_head
# hook_handle = layer4.register_forward_hook(hook)

# model = seg.fcn_resnet50(pretrained=True)
# 设置CAM extractor
cam_extractor = GradCAMpp(model,target_layer='layer4')
# cam_extractor = SmoothGradCAMpp(model,target_layer='decoder')

# 读取图片
img = read_image("../data/cat/2007_002597.jpg")
input_tensor = normalize(resize(img, (224, 224)) / 255., [0.485, 0.456, 0.406], [0.229, 0.224, 0.225])

# 获得模型的输出
out = model(input_tensor.unsqueeze(0))
# print(model)
# print(out.shape)
# print(out.argmax(dim=-1))
# plt.imshow(out[0,0,...].squeeze(0).detach().numpy()); plt.axis('off'); plt.tight_layout(); plt.show()
# plt.imshow(out[0,1,...].squeeze(0).detach().numpy()); plt.axis('off'); plt.tight_layout(); plt.show()
# # 叠加可视化的图
# result = overlay_mask(to_pil_image(img), to_pil_image(out[0,1,...].detach().numpy().squeeze(0), mode='F'), alpha=0.5)
# hook_handle.remove()

# 将模型的输出输入到cam_extractor
activation_map = cam_extractor(out.squeeze(0).argmax().item(),out)

# 可视化激活图
plt.imshow(activation_map[0].squeeze(0).numpy()); plt.axis('off'); plt.tight_layout(); plt.show()

# 可视化叠加图：
result = overlay_mask(to_pil_image(img), to_pil_image(activation_map[0].squeeze(0), mode='F'), alpha=0.5)
plt.imshow(result); plt.axis('off'); plt.tight_layout(); plt.show()