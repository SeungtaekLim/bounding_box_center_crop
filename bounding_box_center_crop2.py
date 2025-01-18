import os
import cv2

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
        
valid_image_length = len(valid_image_files)

# 배치 크기 설정 (100개씩 묶어서 처리)
batch_size = 100

# 각 이미지에 대해 처리 (100개씩 배치로 처리)
for batch_start in range(0, valid_image_length, batch_size):
    batch_end = min(batch_start + batch_size, valid_image_length)  # 마지막 배치는 이미지 개수에 맞게 처리

    # 배치 처리에 대한 출력 (몇 번째 배치인지)
    print(f"처리 중... 배치: {batch_start // batch_size + 1}, 이미지 {batch_start + 1} ~ {batch_end}")

    # 100개씩 처리
    for index1 in range(batch_start, batch_end):
        img_name_without_ext = os.path.splitext(valid_image_files[index1])[0]
        img_path = os.path.join(image_dir, valid_image_files[index1])
        
        # 해당 이미지에 대응하는 텍스트 파일 경로 설정
        txt_file_name = img_name_without_ext + '.txt'
        txt_path = os.path.join(txt_dir, txt_file_name)
        
        # 이미지 읽기
        img = cv2.imread(img_path)
        
        # 이미지 크기 가져오기
        height, width, _ = img.shape

        # 텍스트 파일에서 바운딩 박스 정보 읽기
        with open(txt_path, 'r') as file:
            lines = file.readlines()

        # 자른 이미지의 크기 (2048x2048)
        cropped_width = 2048
        cropped_height = 2048
        
        # 양 옆에서 자를 만큼 계산 (좌우 균등하게 잘라서 중심 기준으로 2048x2048로 자름)
        if width > height:
            start_x = (width - cropped_width) // 2
            start_y = 0
            cropped_image = img[:, start_x:start_x + cropped_width]
        else:
            start_y = (height - cropped_height) // 2
            start_x = 0
            cropped_image = img[start_y:start_y + cropped_height, :]

        # 자른 이미지를 640x640로 리사이즈
        resized_image = cv2.resize(cropped_image, (640, 640))

        # 자른 이미지 저장
        cropped_img_name = f"BGA_{index1 + 1}.png"
        cv2.imwrite(os.path.join(result_dir, cropped_img_name), resized_image)

        # 새로운 텍스트 파일 이름 생성
        new_txt_path = os.path.join(result_dir, f"BGA_{index1 + 1}.txt")

        # 새 텍스트 파일 열기
        with open(new_txt_path, 'w') as new_file:
            for line in lines:
                parts = line.split()

                # 1. 정규화된 좌표를 실제 픽셀 좌표로 변환
                class_id = parts[0]
                center_x_norm = float(parts[1])
                center_y_norm = float(parts[2])
                width_norm = float(parts[3])
                height_norm = float(parts[4])

                center_x_pixel = center_x_norm * width
                center_y_pixel = center_y_norm * height
                width_pixel = width_norm * width
                height_pixel = height_norm * height

                # 2. 자른 영역 기준으로 바운딩 박스 좌표 계산 (자른 이미지 크기에 맞게)
                new_center_x = (center_x_pixel - start_x) / cropped_width
                new_center_y = (center_y_pixel - start_y) / cropped_height
                new_width = width_pixel / cropped_width
                new_height = height_pixel / cropped_height

                # 3. 새로운 라인 작성
                new_line = f"{class_id} {new_center_x} {new_center_y} {new_width} {new_height}\n"
                new_file.write(new_line)

    # 배치마다 완료 메시지 출력
    print(f"배치 {batch_start // batch_size + 1} 처리 완료.")

print("이미지 처리 및 텍스트 변환이 완료되었습니다.")
