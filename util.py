from PIL import Image, ImageTk
import skimage, skimage.io
import torch
import torchvision
import torchxrayvision as xrv
import matplotlib.pyplot as plt
import numpy as np

# Load model
model = xrv.models.DenseNet(weights="densenet121-res224-all")

def load_file(file_path):
    # file_path = "./tests/00000001_000.png"
    if file_path:
        raw_img = skimage.io.imread(f'{file_path}')
        if len(raw_img.shape) > 2:
            raw_img = raw_img[:, :, 0]
        raw_img_pl = Image.fromarray(raw_img).resize(size=[250,250])  
        return raw_img, raw_img_pl

def prediction(raw_img:np.ndarray):
    
    img = xrv.datasets.normalize(raw_img, 255)  
    # Add color channel
    img = img[None, :, :]
    
    transform = torchvision.transforms.Compose([xrv.datasets.XRayCenterCrop(),xrv.datasets.XRayResizer(224)])
    processed_img = transform(img)
    processed_img = torch.from_numpy(processed_img).unsqueeze(0)
                
    with torch.no_grad():
        outputs = model(processed_img)
    probabilities = {class_name: f"{int(p*100)} %" for class_name ,p in zip(model.pathologies,outputs[0].detach().numpy())}
    
    return processed_img, probabilities

def get_heatmap(processed_img,raw_img_pl,class_name):
    processed_img = processed_img.requires_grad_()
    outputs = model(processed_img)
    target = model.pathologies.index(class_name)
    print(outputs[:,target])
    grads = torch.autograd.grad(outputs[:,target], processed_img)[0][0][0]
    blurred = skimage.filters.gaussian(grads.detach().cpu().numpy()**2, sigma= (5, 5), truncate=3.5)
    # blurred_array = ((blurred - blurred.mean())/blurred.std()-0.5)
    blurred_array = ((blurred - blurred.min())/(blurred.max()-blurred.min()))
    
    blurred_array = np.uint8(plt.cm.get_cmap("jet")(blurred_array) * 255)
    heatmap_image = Image.fromarray(blurred_array).resize((250,250))
    heatmap_image.putalpha(128)
    result_img = Image.alpha_composite(raw_img_pl.convert("RGBA"), heatmap_image)
    return result_img