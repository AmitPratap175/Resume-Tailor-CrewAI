#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from job_resume_tailor.crew import JobResumeTailor


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
    'job_posting_url': 'https://www.linkedin.com/jobs/view/4158552671/?refId=%2B3S5eWzF1oVZO1cuJYyU7Q%3D%3D&trackingId=%2B3S5eWzF1oVZO1cuJYyU7Q%3D%3D',
    'github_url': 'https://github.com/AmitPratap175',
    'personal_writeup': """ Amit Pratap is an accomplished Software
    Engineering Leader with 1 year 8 months of experience, specializing 
    in autonomous systems, sensor fusion, and AI-driven control. 
    At Rebhu Computing, he developed sensor calibration pipelines, 
    robust path-tracking algorithms, and AI-powered vehicle autonomy 
    solutions. He has designed state estimation models, neural 
    network-based vehicle controllers, and high-fidelity simulations 
    for drones and unmanned ground vehicles. His work spans drone 
    surveillance, AI-driven defect detection, and intelligent chatbots, 
    bridging AI and robotics for real-world impact.  
    Ideal for leadership roles that require a strategic and 
    innovative approach.""",
    "search_query": ""
}
    
    try:
        JobResumeTailor().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        JobResumeTailor().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        JobResumeTailor().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        JobResumeTailor().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
