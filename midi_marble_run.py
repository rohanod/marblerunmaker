import mido
import pygame
import cv2
import numpy as np

def load_midi(file_path):
    return mido.MidiFile(file_path)

def generate_marble_run(midi_data):
    # Set up constants for the marble run
    FRAME_WIDTH, FRAME_HEIGHT = 1920, 1080
    MARBLE_RADIUS = 10
    TRACK_WIDTH = 30
    NOTE_HEIGHT = 40
    MAX_OCTAVE = 8

    frames = []
    marble_positions = []
    
    for msg in midi_data.play():
        if msg.type == 'note_on' and msg.velocity > 0:
            # Calculate marble position based on the note
            x = int((msg.note % 12) * (FRAME_WIDTH / 12))
            y = FRAME_HEIGHT - (msg.note // 12) * NOTE_HEIGHT
            
            # Create a frame with the new marble
            frame = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
            
            # Draw tracks
            for i in range(12):
                track_x = int(i * (FRAME_WIDTH / 12))
                cv2.line(frame, (track_x, 0), (track_x, FRAME_HEIGHT), (50, 50, 50), TRACK_WIDTH)
            
            # Draw existing marbles
            for pos in marble_positions:
                cv2.circle(frame, pos, MARBLE_RADIUS, (255, 255, 255), -1)
            
            # Draw new marble
            cv2.circle(frame, (x, y), MARBLE_RADIUS, (0, 255, 0), -1)
            
            marble_positions.append((x, y))
            frames.append(frame)
            
            # Move existing marbles down
            marble_positions = [(x, min(y + NOTE_HEIGHT, FRAME_HEIGHT - MARBLE_RADIUS)) for x, y in marble_positions]
    
    return frames

def create_video(frames, output_path, fps=30):
    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for frame in frames:
        out.write(frame)
    
    out.release()

def main(midi_file_path, output_video_path):
    midi_data = load_midi(midi_file_path)
    frames = generate_marble_run(midi_data)
    create_video(frames, output_video_path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python midi_marble_run.py <input_midi_file> <output_video_file>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])