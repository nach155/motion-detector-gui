def crop_image_array(image_array, top_left, bottom_right):
    """
    左上と右下のピクセル座標で画像配列をトリミングします。
    Parameters:
        image_array (np.ndarray): トリミング対象の画像配列 (H, W, C) または (H, W)
        top_right (tuple): トリミング範囲の右上座標 (row, col)
        bottom_left (tuple): トリミング範囲の左下座標 (row, col)

    Returns:
        np.ndarray: トリミング後の画像配列
    """
    top_row, left_col = top_left
    bottom_row, right_col = bottom_right
    return image_array[
        min(left_col,right_col):max(left_col,right_col),
        min(top_row,bottom_row):max(top_row,bottom_row),
    ]