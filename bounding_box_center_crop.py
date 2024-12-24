import os
import cv2

def process_images_and_text(class_name):
    base_dir = os.getcwd()

    # 이미지 및 텍스트 폴더 경로 설정
    image_dir = os.path.join(base_dir, 'image')
    txt_dir = os.path.join(base_dir, 'txt')
    result_dir = os.path.join(base_dir, 'result')

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    image_files = [f for f in os.listdir(image_dir) if f.endswith('.png') or f.endswith('.jpg')]
    txt_files = [f for f in os.listdir(txt_dir) if f.endswith('.txt')]

    valid_image_files = []

    # 이미지 파일과 대응하는 텍스트 파일이 있는지 확인
    for img_file in image_files:
        img_name_without_ext = os.path.splitext(img_file)[0]
        txt_file_name = img_name_without_ext + '.txt'
        
        # 텍스트 파일이 존재하고 비어있지 않으면 유효한 이미지로 추가
        if txt_file_name in txt_files and os.path.getsize(os.path.join(txt_dir, txt_file_name)) > 0:
            valid_image_files.append(img_file)
        else:
            print(f"건너뜁니다: 이미지 파일 {img_file}에 대응하는 텍스트 파일이 없거나 비어 있습니다.")

    for index1, img_file in enumerate(valid_image_files):
        img_name_without_ext = os.path.splitext(img_file)[0]
        img_path = os.path.join(image_dir, img_file)
        
        txt_file_name = img_name_without_ext + '.txt'
        txt_path = os.path.join(txt_dir, txt_file_name)
        
        img = cv2.imread(img_path)
        
        height, width, _ = img.shape

        center_x, center_y = None, None
        with open(txt_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.split()
                class_id = int(parts[0])

                if parts[0] == class_name:
                    center_x = float(parts[1]) * width
                    center_y = float(parts[2]) * height
                    break

        if center_x is None or center_y is None:
            print(f"경고: 이미지 {img_file}에서 클래스 {class_name}을 찾을 수 없습니다.")
            continue

        start_x = int(center_x - 320)
        start_y = int(center_y - 320)
        end_x = int(center_x + 320)
        end_y = int(center_y + 320)

        cropped_image = img[start_y:end_y, start_x:end_x]

        cropped_img_name = f"qfn_{index1 + 1}.png"
        cv2.imwrite(os.path.join(result_dir, cropped_img_name), cropped_image)

        with open(txt_path, 'r') as file:
            lines = file.readlines()

        new_txt_path = os.path.join(result_dir, f"qfn_{index1 + 1}.txt")

        with open(new_txt_path, 'w') as new_file:
            for line in lines:
                parts = line.split()


                class_id = parts[0]
                center_x_norm = float(parts[1])
                center_y_norm = float(parts[2])
                width_norm = float(parts[3])
                height_norm = float(parts[4])

                new_center_x = (center_x_norm * width - start_x) / 640
                new_center_y = (center_y_norm * height - start_y) / 640
                new_width = width_norm * width / 640
                new_height = height_norm * height / 640

                new_line = f"{class_id} {new_center_x} {new_center_y} {new_width} {new_height}\n"
                new_file.write(new_line)

    print(f"클래스 {class_name}에 대한 이미지 처리 및 텍스트 변환이 완료되었습니다.")
