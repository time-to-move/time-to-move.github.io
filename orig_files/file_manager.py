#!/usr/bin/env python3
"""
Script to rename video files in DL3DV directory according to specified mapping:
gt_4_video -> GroundTruth
output_gwtf -> GWTF
sample -> Ours
warped_4_video -> Warped
"""

import os
import argparse
import sys
import subprocess
from pathlib import Path
import cv2
import numpy as np

def rename_videos_in_dl3dv(base_path="DL3DV"):
    """
    Rename video files in all subdirectories of DL3DV according to the mapping.
    
    Args:
        base_path (str): Path to the DL3DV directory
    """
    
    # Define the renaming mapping
    rename_mapping = {
        "gt_4_video.mp4": "GroundTruth.mp4",
        "output_gwtf.mp4": "GWTF.mp4", 
        "sample.mp4": "Ours.mp4",
        "warped_4_video.mp4": "Warped.mp4"
    }
    
    # Check if DL3DV directory exists
    dl3dv_path = Path(base_path)
    if not dl3dv_path.exists():
        print(f"Error: Directory '{base_path}' does not exist!")
        return False
    
    # Get all subdirectories in DL3DV
    subdirs = [d for d in dl3dv_path.iterdir() if d.is_dir()]
    
    if not subdirs:
        print(f"No subdirectories found in '{base_path}'")
        return False
    
    print(f"Found {len(subdirs)} subdirectories in '{base_path}'")
    
    total_renamed = 0
    errors = []
    
    # Process each subdirectory
    for subdir in subdirs:
        print(f"\nProcessing directory: {subdir.name}")
        
        # Rename files in this subdirectory
        for old_name, new_name in rename_mapping.items():
            old_path = subdir / old_name
            new_path = subdir / new_name
            
            if old_path.exists():
                try:
                    old_path.rename(new_path)
                    print(f"  ✓ Renamed: {old_name} -> {new_name}")
                    total_renamed += 1
                except Exception as e:
                    error_msg = f"  ✗ Failed to rename {old_name}: {e}"
                    print(error_msg)
                    errors.append(f"{subdir.name}/{old_name}: {e}")
            else:
                print(f"  - File not found: {old_name}")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Renaming completed!")
    print(f"Total files renamed: {total_renamed}")
    
    if errors:
        print(f"Errors encountered: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
    else:
        print("No errors encountered!")
    
    return len(errors) == 0


def rename_mcbench_videos(base_path="MC-Bench"):
    """
    Rename videos in MC-Bench directory by extracting mp4 files from subdirectories.
    For each ID folder, if any *.mp4 file is actually a directory, extract the single mp4
    file from it and rename it to the directory name.
    
    Args:
        base_path (str): Path to the MC-Bench directory
    """
    
    # Check if MC-Bench directory exists
    mc_bench_path = Path(base_path)
    if not mc_bench_path.exists():
        print(f"Error: Directory '{base_path}' does not exist!")
        return False
    
    # Get all subdirectories in MC-Bench
    subdirs = [d for d in mc_bench_path.iterdir() if d.is_dir()]
    
    if not subdirs:
        print(f"No subdirectories found in '{base_path}'")
        return False
    
    print(f"Found {len(subdirs)} subdirectories in '{base_path}'")
    
    total_processed = 0
    errors = []
    
    # Process each subdirectory
    for subdir in subdirs:
        print(f"\nProcessing directory: {subdir.name}")
        
        # Look for mp4 files/directories
        mp4_items = list(subdir.glob("*.mp4"))
        
        for mp4_item in mp4_items:
            if mp4_item.is_dir():
                print(f"  Found directory named: {mp4_item.name}")
                
                # Check if there's exactly one mp4 file inside
                mp4_files_inside = list(mp4_item.glob("*.mp4"))
                
                if len(mp4_files_inside) == 1:
                    mp4_file = mp4_files_inside[0]
                    temp_path = subdir / f"temp_{mp4_item.name}"
                    target_path = subdir / mp4_item.name
                    
                    try:
                        # Move the file to a temporary name first
                        mp4_file.rename(temp_path)
                        print(f"    ✓ Moved: {mp4_file.name} -> temp_{mp4_item.name}")
                        
                        # Remove the empty directory
                        mp4_item.rmdir()
                        print(f"    ✓ Removed directory: {mp4_item.name}")
                        
                        # Now rename to the final target name
                        temp_path.rename(target_path)
                        print(f"    ✓ Renamed: temp_{mp4_item.name} -> {mp4_item.name}")
                        
                        total_processed += 1
                        
                    except Exception as e:
                        error_msg = f"    ✗ Failed to process {mp4_item.name}: {e}"
                        print(error_msg)
                        errors.append(f"{subdir.name}/{mp4_item.name}: {e}")
                        # Clean up temp file if it exists
                        if temp_path.exists():
                            temp_path.unlink()
                        
                elif len(mp4_files_inside) == 0:
                    print(f"    - No mp4 files found in directory: {mp4_item.name}")
                    errors.append(f"{subdir.name}/{mp4_item.name}: No mp4 files found")
                else:
                    print(f"    - Multiple mp4 files found in directory: {mp4_item.name}")
                    errors.append(f"{subdir.name}/{mp4_item.name}: Multiple mp4 files found")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"MC-Bench renaming completed!")
    print(f"Total directories processed: {total_processed}")
    
    if errors:
        print(f"Errors encountered: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
    else:
        print("No errors encountered!")
    
    return len(errors) == 0


def crop_frame(frame: np.ndarray, crop_params: dict) -> np.ndarray:
    """
    Crop a frame according to the specified parameters.
    
    Args:
        frame: Input frame as numpy array
        crop_params: Dictionary with 'x', 'y', 'w', 'h' keys
        
    Returns:
        Cropped frame as numpy array
    """
    x, y, w, h = crop_params['x'], crop_params['y'], crop_params['w'], crop_params['h']
    
    # Handle special cases where w or h are 0 (meaning crop to end)
    if y + h == 0:
        h = frame.shape[0] - y
    if x + w == 0:
        w = frame.shape[1] - x
    
    # Perform the crop
    frame = frame[y:y+h, x:x+w]
    
    return frame


def resize_frame_to_height(frame: np.ndarray, target_height: int) -> np.ndarray:
    """
    Resize a frame to a target height while maintaining aspect ratio.
    
    Args:
        frame: Input frame as numpy array
        target_height: Target height in pixels
        
    Returns:
        Resized frame as numpy array
    """
    h, w = frame.shape[:2]
    aspect_ratio = w / h
    target_width = int(target_height * aspect_ratio)
    
    return cv2.resize(frame, (target_width, target_height))


def concatenate_videos_horizontally(video_paths: list, output_path: str, target_height: int = 320, duplicate_frames: bool = False) -> bool:
    """
    Concatenate multiple videos horizontally into a single video.
    
    Args:
        video_paths: List of paths to video files
        output_path: Path for the output concatenated video
        target_height: Target height for all videos (they will be resized to this height)
        duplicate_frames: If True, duplicate each frame to slow down the video
        
    Returns:
        True if successful, False otherwise
    """
    if not video_paths:
        print("No video paths provided")
        return False
    
    # Open all video captures
    caps = []
    for video_path in video_paths:
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            print(f"Failed to open video: {video_path}")
            # Close already opened captures
            for c in caps:
                c.release()
            return False
        caps.append(cap)
    
    try:
        # Get video properties from the first video
        fps = int(caps[0].get(cv2.CAP_PROP_FPS))
        total_frames = int(caps[0].get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Calculate total width
        total_width = 0
        frame_widths = []
        
        # Read first frame from each video to calculate dimensions
        first_frames = []
        for i, cap in enumerate(caps):
            ret, frame = cap.read()
            if not ret:
                print(f"Failed to read first frame from video {i}")
                return False
            
            resized_frame = resize_frame_to_height(frame, target_height)
            frame_width = resized_frame.shape[1]
            frame_widths.append(frame_width)
            total_width += frame_width
            first_frames.append(resized_frame)
            
            # Reset to beginning
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        # Create output video writer with better codec
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (total_width, target_height))
        
        if not out.isOpened():
            print(f"Failed to create output video writer: {output_path}")
            # Try alternative codec
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(output_path.replace('.mp4', '.avi'), fourcc, fps, (total_width, target_height))
            if not out.isOpened():
                print(f"Failed to create output video writer with alternative codec")
                return False
        
        print(f"Concatenating videos: {len(video_paths)} videos")
        print(f"Output dimensions: {total_width}x{target_height}")
        print(f"Total frames: {total_frames}")
        
        # Debug: Check frame counts for each video
        for i, cap in enumerate(caps):
            frame_count_vid = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            print(f"  Video {i}: {frame_count_vid} frames")
        
        # Process all frames
        frame_count = 0
        while True:
            frames = []
            all_read_successfully = True
            
            # Read frame from each video
            for i, cap in enumerate(caps):
                ret, frame = cap.read()
                if not ret:
                    if frame_count == 0:
                        print(f"  Warning: Video {i} has no frames or failed to read")
                    all_read_successfully = False
                    break
                
                # Resize frame to target height
                resized_frame = resize_frame_to_height(frame, target_height)
                frames.append(resized_frame)
            
            if not all_read_successfully:
                break
            
            # Concatenate frames horizontally
            concatenated_frame = np.concatenate(frames, axis=1)
            
            # Write the concatenated frame
            out.write(concatenated_frame)
            frame_count += 1
            
            # If duplicate_frames is True, write the frame again to slow down the video
            if duplicate_frames:
                out.write(concatenated_frame)
                frame_count += 1
            
            if frame_count % 10 == 0:  # Progress update every 10 frames
                print(f"  Processed {frame_count}/{total_frames * (2 if duplicate_frames else 1)} frames")
        
        # Clean up
        for cap in caps:
            cap.release()
        out.release()
        
        print(f"✓ Concatenated video saved as: {output_path}")
        print(f"  Processed {frame_count} frames")
        
        return True
        
    except Exception as e:
        print(f"Error during concatenation: {e}")
        # Clean up
        for cap in caps:
            cap.release()
        return False


def concatenate_mcbench_videos(base_path="MC-Bench"):
    """
    Concatenate videos in MC-Bench directory horizontally.
    Order: Warped, Ours_SVD, Drag_Anything, SGI2V, MotionPro
    
    Args:
        base_path (str): Path to the MC-Bench directory
    """
    
    # MC-Bench video order and filenames
    video_files = [
        "Warped.mp4",
        "Ours_SVD.mp4", 
        "Drag_Anything.mp4",
        "SGI2V.mp4",
        "MotionPro_cropped.mp4"
    ]
    
    # Check if MC-Bench directory exists
    mc_bench_path = Path(base_path)
    if not mc_bench_path.exists():
        print(f"Error: Directory '{base_path}' does not exist!")
        return False
    
    # Get all subdirectories in MC-Bench
    subdirs = [d for d in mc_bench_path.iterdir() if d.is_dir()]
    
    if not subdirs:
        print(f"No subdirectories found in '{base_path}'")
        return False
    
    print(f"Found {len(subdirs)} subdirectories in '{base_path}'")
    print(f"Concatenating videos in order: {', '.join(video_files)}")
    
    total_processed = 0
    errors = []
    
    # Process each subdirectory
    for subdir in subdirs:
        print(f"\nProcessing directory: {subdir.name}")
        
        # Check if all required videos exist
        video_paths = []
        missing_videos = []
        
        for video_file in video_files:
            video_path = subdir / video_file
            if video_path.exists():
                video_paths.append(video_path)
            else:
                missing_videos.append(video_file)
        
        if missing_videos:
            print(f"  ✗ Missing videos: {', '.join(missing_videos)}")
            errors.append(f"{subdir.name}: Missing videos {', '.join(missing_videos)}")
            continue
        
        # Create output path
        output_path = subdir / "concatenated.mp4"
        
        try:
            # Concatenate videos horizontally
            success = concatenate_videos_horizontally(video_paths, str(output_path))
            
            if success:
                total_processed += 1
            else:
                errors.append(f"{subdir.name}: Failed to concatenate videos")
                
        except Exception as e:
            error_msg = f"  ✗ Failed to concatenate videos: {e}"
            print(error_msg)
            errors.append(f"{subdir.name}: {e}")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"MC-Bench concatenation completed!")
    print(f"Total directories processed: {total_processed}")
    
    if errors:
        print(f"Errors encountered: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
    else:
        print("No errors encountered!")
    
    return len(errors) == 0


def concatenate_dl3dv_videos(base_path="DL3DV"):
    """
    Concatenate videos in DL3DV directory horizontally.
    Order: Warped, Ours, GWTF, GroundTruth
    
    Args:
        base_path (str): Path to the DL3DV directory
    """
    
    # DL3DV video order and filenames (try renamed versions first, then original names)
    video_files = [
        "Warped.mp4",
        "Ours.mp4",
        "GWTF.mp4", 
        "GroundTruth.mp4"
    ]
    
    # Check if DL3DV directory exists
    dl3dv_path = Path(base_path)
    if not dl3dv_path.exists():
        print(f"Error: Directory '{base_path}' does not exist!")
        return False
    
    # Get all subdirectories in DL3DV
    subdirs = [d for d in dl3dv_path.iterdir() if d.is_dir()]
    
    if not subdirs:
        print(f"No subdirectories found in '{base_path}'")
        return False
    
    print(f"Found {len(subdirs)} subdirectories in '{base_path}'")
    print(f"Concatenating videos in order: Warped, Ours, GWTF, GroundTruth")
    
    total_processed = 0
    errors = []
    
    # Process each subdirectory
    for subdir in subdirs:
        print(f"\nProcessing directory: {subdir.name}")
        
        # Check if all required videos exist
        video_paths = []
        missing_videos = []
        
        for video_file in video_files:
            video_path = subdir / video_file
            if video_path.exists():
                video_paths.append(video_path)
            else:
                missing_videos.append(video_file)
        
        if missing_videos:
            print(f"  ✗ Missing videos: {', '.join(missing_videos)}")
            errors.append(f"{subdir.name}: Missing videos {', '.join(missing_videos)}")
            continue
        
        # Create output path
        output_path = subdir / "concatenated.mp4"
        
        try:
            # Concatenate videos horizontally
            success = concatenate_videos_horizontally(video_paths, str(output_path))
            
            if success:
                total_processed += 1
            else:
                errors.append(f"{subdir.name}: Failed to concatenate videos")
                
        except Exception as e:
            error_msg = f"  ✗ Failed to concatenate videos: {e}"
            print(error_msg)
            errors.append(f"{subdir.name}: {e}")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"DL3DV concatenation completed!")
    print(f"Total directories processed: {total_processed}")
    
    if errors:
        print(f"Errors encountered: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
    else:
        print("No errors encountered!")
    
    return len(errors) == 0


def concatenate_user_videos(base_path="UserCameraControl", object_path="UserObjectControl"):
    """
    Concatenate pairs of warped/ours videos from UserCameraControl and UserObjectControl directories.
    
    Args:
        base_path (str): Path to the UserCameraControl directory
        object_path (str): Path to the UserObjectControl directory
    """
    
    # Check if both directories exist
    camera_path = Path(base_path)
    object_path = Path(object_path)
    
    if not camera_path.exists():
        print(f"Error: Directory '{base_path}' does not exist!")
        return False
    
    if not object_path.exists():
        print(f"Error: Directory '{object_path}' does not exist!")
        return False
    
    # Get all video files from both directories
    camera_videos = [f for f in list(camera_path.glob("*.mp4")) if f.is_file() and "concatenated" not in f.name]
    object_videos = [f for f in list(object_path.glob("*.mp4")) if f.is_file() and "concatenated" not in f.name]
    
    print(f"Found {len(camera_videos)} videos in {base_path}")
    print(f"Found {len(object_videos)} videos in {object_path}")
    
    # Create pairs by matching video names with flexible matching
    pairs_found = []
    camera_processed = set()
    object_processed = set()
    def normalize_name(name):
            """Normalize video names for better matching"""
            return name[:name.find('_')].lower()
    
    def find_pairs_in_directory(videos):
        """Find pairs of warped/ours videos within a single directory"""
        
        pairs = {}
        for video in videos:
            video_name = normalize_name(video.stem)
            if "our" in video.name:
                if video_name not in pairs:
                    pairs[video_name] = {"ours": video}
                else:
                    pairs[video_name]["ours"] = video
                    if "unknown" in pairs[video_name]:
                        pairs[video_name]["warped"] = video
                        del pairs[video_name]["unknown"]
            elif "warped" in video.name:
                if video_name not in pairs:
                    pairs[video_name] = {"warped": video}
                else:
                    pairs[video_name]["warped"] = video
                    if "unknown" in pairs[video_name]:
                        pairs[video_name]["ours"] = video
                        del pairs[video_name]["unknown"]
            else:
                if video_name not in pairs:
                    pairs[video_name] = {"unknown": video}
                else:
                    other_name = list(pairs[video_name].keys())[0]
                    if other_name == "ours":
                        pairs[video_name]["warped"] = video
                    elif other_name == "warped":
                        pairs[video_name]["ours"] = video
                    else:
                        print("Found two unknown videos with the same name: ", video_name)
                        raise ValueError("Found two unknown videos with the same name: ", video_name)
        
        return pairs
    
    # Find pairs in each directory separately
    camera_pairs = find_pairs_in_directory(camera_videos)
    object_pairs = find_pairs_in_directory(object_videos)
    
    print(f"Found {len(camera_pairs)} pairs in {base_path}")
    print(f"Found {len(object_pairs)} pairs in {object_path}")
    
    # Process camera pairs
    pairs_found = []
    camera_processed = set()
    
    for pair_name, pair_videos in camera_pairs.items():
        if "ours" in pair_videos and "warped" in pair_videos:
            pairs_found.append((pair_videos["warped"], pair_videos["ours"]))
            camera_processed.add(pair_videos["warped"])
            camera_processed.add(pair_videos["ours"])
        else:
            missing_type = "warped" if "ours" in pair_videos else "ours"
            print(f"  ⚠ Warning: Missing {missing_type} video for {pair_name}")
    
    # Process object pairs
    object_processed = set()
    
    for pair_name, pair_videos in object_pairs.items():
        if "ours" in pair_videos and "warped" in pair_videos:
            pairs_found.append((pair_videos["warped"], pair_videos["ours"]))
            object_processed.add(pair_videos["warped"])
            object_processed.add(pair_videos["ours"])
        else:
            missing_type = "warped" if "ours" in pair_videos else "ours"
            print(f"  ⚠ Warning: Missing {missing_type} video for {pair_name}")
    
    # Check for unmatched videos
    unmatched_camera = set(camera_videos) - camera_processed
    unmatched_object = set(object_videos) - object_processed
    
    if unmatched_camera:
        print(f"  ⚠ Warning: Unmatched camera videos: {[v.name for v in unmatched_camera]}")
    if unmatched_object:
        print(f"  ⚠ Warning: Unmatched object videos: {[v.name for v in unmatched_object]}")
    
    if not pairs_found:
        print("No matching video pairs found!")
        return False
    
    print(f"\nFound {len(pairs_found)} matching video pairs")
    
    total_processed = 0
    errors = []
    
    # Process each pair
    for warped_video, ours_video in pairs_found:
        print(f"\nProcessing pair: {warped_video.name} + {ours_video.name}")
        
        # Create output path (use normalized video name, determine directory)
        normalized_name = normalize_name(warped_video.stem)
        if warped_video.parent == camera_path:
            output_path = camera_path / f"{normalized_name}_concatenated.mp4"
        else:
            output_path = object_path / f"{normalized_name}_concatenated.mp4"
        
        try:
            # Determine if this is a camera control video (from UserCameraControl directory)
            is_camera_control = warped_video.parent == camera_path
            
            # Concatenate videos horizontally with frame duplication for camera control videos
            success = concatenate_videos_horizontally([warped_video, ours_video], str(output_path), duplicate_frames=is_camera_control)
            
            if success:
                total_processed += 1
                if is_camera_control:
                    print(f"  ✓ Camera control video - frames duplicated for slower playback")
            else:
                errors.append(f"{warped_video.name} + {ours_video.name}: Failed to concatenate")
                
        except Exception as e:
            error_msg = f"  ✗ Failed to concatenate {warped_video.name} + {ours_video.name}: {e}"
            print(error_msg)
            errors.append(f"{warped_video.name} + {ours_video.name}: {e}")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"User video concatenation completed!")
    print(f"Total pairs processed: {total_processed}")
    
    if errors:
        print(f"Errors encountered: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
    else:
        print("No errors encountered!")
    
    return len(errors) == 0


def reencode_concatenated_videos(base_path=".", overwrite_for_rencode=False):
    """
    Recursively find all concatenated.mp4 files and re-encode them for better browser compatibility.
    
    Args:
        base_path (str): Path to start searching from (default: current directory)
    """
    
    base_path = Path(base_path)
    if not base_path.exists():
        print(f"Error: Directory '{base_path}' does not exist!")
        return False
    
    print(f"Searching for concatenated.mp4 files in: {base_path}")
    
    # Find all concatenated.mp4 files recursively
    concatenated_files = list(base_path.rglob("*concatenated.mp4"))
    
    if not concatenated_files:
        print("No concatenated.mp4 files found!")
        return True
    
    print(f"Found {len(concatenated_files)} concatenated.mp4 files")
    
    total_processed = 0
    errors = []
    
    # Process each file
    for video_file in concatenated_files:
        print(f"\nProcessing: {video_file}")
        
        # Create output filename
        output_file = video_file.parent / video_file.name.replace("concatenated.mp4", "concatenated_fixed.mp4")
        if output_file.exists() and not overwrite_for_rencode:
            print(f"  Skipping: {output_file} already exists")
            continue
        elif output_file.exists() and overwrite_for_rencode:
            print(f"  Overwriting: {output_file}")
            os.remove(output_file)
        
        try:
            # Build ffmpeg command
            cmd = [
                "ffmpeg",
                "-i", str(video_file),
                "-c:v", "libx264",
                "-crf", "23",
                "-preset", "fast",
                "-movflags", "+faststart",
                str(output_file)
            ]
            
            print(f"  Running: {' '.join(cmd)}")
            
            # Run ffmpeg command
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"  ✓ Successfully re-encoded: {output_file.name}")
                total_processed += 1
                
                # Optionally remove original file (uncomment if desired)
                # video_file.unlink()
                # print(f"  ✓ Removed original file: {video_file.name}")
                
            else:
                error_msg = f"  ✗ FFmpeg failed: {result.stderr}"
                print(error_msg)
                errors.append(f"{video_file}: {result.stderr}")
                
        except FileNotFoundError:
            error_msg = "  ✗ FFmpeg not found! Please install FFmpeg and ensure it's in your PATH"
            print(error_msg)
            errors.append(f"{video_file}: FFmpeg not found")
        except Exception as e:
            error_msg = f"  ✗ Failed to process {video_file}: {e}"
            print(error_msg)
            errors.append(f"{video_file}: {e}")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Re-encoding completed!")
    print(f"Total files processed: {total_processed}")
    
    if errors:
        print(f"Errors encountered: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
    else:
        print("No errors encountered!")
    
    return len(errors) == 0


def crop_motionpro_videos(base_path="MC-Bench"):
    """
    Crop MotionPro videos in MC-Bench directory according to specified parameters.
    
    Args:
        base_path (str): Path to the MC-Bench directory
    """
    
    # MotionPro crop parameters
    crop_params = {'x': -512, 'y': 0, 'w': 512, 'h': 320}
    
    # Check if MC-Bench directory exists
    mc_bench_path = Path(base_path)
    if not mc_bench_path.exists():
        print(f"Error: Directory '{base_path}' does not exist!")
        return False
    
    # Get all subdirectories in MC-Bench
    subdirs = [d for d in mc_bench_path.iterdir() if d.is_dir()]
    
    if not subdirs:
        print(f"No subdirectories found in '{base_path}'")
        return False
    
    print(f"Found {len(subdirs)} subdirectories in '{base_path}'")
    print(f"Cropping MotionPro videos with parameters: {crop_params}")
    
    total_processed = 0
    errors = []
    
    # Process each subdirectory
    for subdir in subdirs:
        print(f"\nProcessing directory: {subdir.name}")
        
        motionpro_file = subdir / "MotionPro.mp4"
        
        if motionpro_file.exists():
            try:
                # Read the video
                cap = cv2.VideoCapture(str(motionpro_file))
                
                if not cap.isOpened():
                    print(f"  ✗ Failed to open video: {motionpro_file}")
                    errors.append(f"{subdir.name}/MotionPro.mp4: Failed to open video")
                    continue
                
                # Get video properties
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                
                print(f"  Video properties: {width}x{height}, {fps} FPS, {total_frames} frames")
                
                # Determine crop parameters based on aspect ratio
                if height == 512:  # Flipped aspect ratio (512x320)
                    print(f"  Detected flipped aspect ratio, adjusting crop parameters")
                    crop_params_adjusted = {'x': -320, 'y': 0, 'w': 320, 'h': 512}
                else:  # Normal aspect ratio (320x512)
                    crop_params_adjusted = crop_params
                
                # Create output video writer
                output_file = subdir / "MotionPro_cropped.mp4"
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                
                # Calculate output dimensions
                output_width = 512 if height != 512 else 320
                output_height = height
                
                out = cv2.VideoWriter(str(output_file), fourcc, fps, (output_width, output_height))
                
                if not out.isOpened():
                    print(f"  ✗ Failed to create output video writer")
                    cap.release()
                    errors.append(f"{subdir.name}/MotionPro.mp4: Failed to create output writer")
                    continue
                
                # Process frames
                frame_count = 0
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # Crop the frame
                    cropped_frame = crop_frame(frame, crop_params_adjusted)
                    
                    # Write the cropped frame
                    out.write(cropped_frame)
                    frame_count += 1
                    
                    if frame_count % 30 == 0:  # Progress update every 30 frames
                        print(f"    Processed {frame_count}/{total_frames} frames")
                
                # Clean up
                cap.release()
                out.release()
                
                print(f"  ✓ Cropped video saved as: MotionPro_cropped.mp4")
                print(f"    Output dimensions: {output_width}x{output_height}")
                print(f"    Processed {frame_count} frames")
                
                total_processed += 1
                
            except Exception as e:
                error_msg = f"  ✗ Failed to process MotionPro video: {e}"
                print(error_msg)
                errors.append(f"{subdir.name}/MotionPro.mp4: {e}")
        else:
            print(f"  - MotionPro.mp4 not found in {subdir.name}")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Cropping completed!")
    print(f"Total videos processed: {total_processed}")
    
    if errors:
        print(f"Errors encountered: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
    else:
        print("No errors encountered!")
    
    return len(errors) == 0


def main():
    """Main function to run the renaming script."""
    parser = argparse.ArgumentParser(description="Rename and move around videos script.")
    parser.add_argument("--rn_dl3dv", action="store_true", help="Rename all videos in DL3DV directory.")
    parser.add_argument("--rn_mcbench", action="store_true", help="Rename videos in MC-Bench directory by extracting from subdirectories.")
    parser.add_argument("--crop_motionpro", action="store_true", help="Crop MotionPro videos in MC-Bench directory.")
    parser.add_argument("--concat_mcbench", action="store_true", help="Concatenate videos horizontally in MC-Bench directory.")
    parser.add_argument("--concat_dl3dv", action="store_true", help="Concatenate videos horizontally in DL3DV directory.")
    parser.add_argument("--concat_user", action="store_true", help="Concatenate pairs of videos from UserCameraControl and UserObjectControl directories.")
    parser.add_argument("--rencode_concat", action="store_true", help="Re-encode all concatenated.mp4 files for better browser compatibility.")
    parser.add_argument("--overwrite_for_rencode", action="store_true", help="Overwrite the original concatenated.mp4 files for re-encoding.")
    args = parser.parse_args()
    
    if args.rn_dl3dv:
        if not rename_videos_in_dl3dv():
            print("Failed to rename videos in DL3DV directory.")
    elif args.rn_mcbench:
        if not rename_mcbench_videos():
            print("Failed to rename videos in MC-Bench directory.")
    elif args.crop_motionpro:
        if not crop_motionpro_videos():
            print("Failed to crop MotionPro videos in MC-Bench directory.")
    elif args.concat_mcbench:
        if not concatenate_mcbench_videos():
            print("Failed to concatenate videos in MC-Bench directory.")
    elif args.concat_dl3dv:
        if not concatenate_dl3dv_videos():
            print("Failed to concatenate videos in DL3DV directory.")
    elif args.concat_user:
        if not concatenate_user_videos():
            print("Failed to concatenate user videos.")
    elif args.rencode_concat:
        if not reencode_concatenated_videos(overwrite_for_rencode=args.overwrite_for_rencode):
            print("Failed to re-encode concatenated videos.")
    else:
        print("No action specified. see --help for available options.")

if __name__ == "__main__":
    main()
