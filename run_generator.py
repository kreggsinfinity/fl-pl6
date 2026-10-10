import sys
import asyncio
from mistakes_generator import run_mistakes_generation

def main():
    print("Starting Common Mistakes Fixer generator (9:16 Vertical Reel)...")
    video_p, meta = asyncio.run(run_mistakes_generation(idx=0))
    print(f"Done! Final video generated: {video_p}")

if __name__ == "__main__":
    main()
