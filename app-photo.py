import vertexai
from vertexai.preview.vision_models import Image, ImageGenerationModel

# TODO(developer): Update and un-comment below lines
project_id = "techtonic-383914"
input_file = r"C:\Users\User\Pictures\Screenshots\1.png"
output_file = r"C:\Users\User\Pictures\Screenshots\11.png"
# The text prompt describing what you want to see.
prompt = "這是一台氣炸鍋，請生成視覺產品圖，去背，真實，居家，廚房"

vertexai.init(project=project_id, location="us-central1")

model = ImageGenerationModel.from_pretrained("imagegeneration@002")
base_img = Image.load_from_file(location=input_file)

images = model.edit_image(
    base_image=base_img,
    prompt=prompt,
    # Optional parameters
    seed=1,
    # Controls the strength of the prompt.
    # -- 0-9 (low strength), 10-20 (medium strength), 21+ (high strength)
    guidance_scale=21,
    number_of_images=1,
)
#for迴圈產出5張圖（需增加寫程式）

images[0].save(location=output_file, include_generation_parameters=False)

# Optional. View the edited image in a notebook.
# images[0].show()

print(f"Created output image using {len(images[0]._image_bytes)} bytes")


#產出多張圖
#手動挑