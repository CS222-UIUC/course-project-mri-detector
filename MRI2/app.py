from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import torch
from torchvision import datasets, transforms
from linformer import Linformer
from vit_pytorch.efficient import ViT
import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


app = Flask(__name__)

def loadModel(file, img):
  device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
  efficient_transformer = Linformer(
    dim=128,
    seq_len = 49+1, #7x7 patches + 1 cls-token
    depth=12,
    heads=8,
    k=64
  )

  model = ViT(
    dim=128,
    image_size=224,
    patch_size=32,
    num_classes=2,
    transformer=efficient_transformer,
    channels=1
  ).to(device)

  checkpoint_path = "model_checkpoint.pth"

  model.load_state_dict(torch.load(checkpoint_path))
  model.eval()

  with torch.inference_mode():
    predict_img = img
    # predict_img = cv2.cvtColor(predict_img, cv2.COLOR_BGR2GRAY)
    predict_img = cv2.resize(predict_img, (256, 256))
    # cv2.imwrite(predict_img_path, predict_img)

    transformer = transforms.Compose(
        [
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
        ])
    
    predict_img = Image.open(file)

    predict_img_tensor = transformer(predict_img)
    predict_img_tensor = predict_img_tensor.view(1, 1, 224, 224)

    prediction = model(predict_img_tensor)
    
    classification_prediction = "true" if np.argmax(prediction)==1 else "false"
    
    plt.imshow(predict_img, cmap='gray')
    plt.title(f'Prediction: {classification_prediction}')
    plt.savefig('static/plot.png')
    # plt.show()

# Define the file upload route
@app.route('/upload', methods=['POST'])
def upload():
  f = request.files['mri']
  file = f.read()
  file_bytes = np.fromstring(file, np.uint8)
  img = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)
  # print("Type: ", type(file))
  # image = Image.open(file)
  # image.show()
  loadModel(f, img)
  return redirect(url_for('index'))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/post', methods=['POST'])
def post():
    return "recived: {}".format(request.form)

if __name__ == "__main__":
    app.run(debug=False)