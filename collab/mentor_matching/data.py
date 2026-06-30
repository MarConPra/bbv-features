import json
import os
from uuid import uuid4
from .models import Mentor, Project, ProjectInput, ProjectGoal
from .embedding import embed_texts, build_mentor_text, build_project_text


SEED_MENTORS = [
    Mentor(
        id=uuid4(),
        name="Dr. Arjun Mehta",
        email="amehta@iitd.ac.in",
        affiliation="IIT Delhi",
        department="Computer Science & Engineering",
        designation="Professor",
        domain="machine learning",
        research_areas=["deep learning", "NLP", "computer vision", "medical imaging"],
        bio="Leading researcher in deep learning for medical image analysis with 15+ years of experience.",
        h_index=38,
        total_publications=120,
        recent_publications_2yr=12,
        publication_titles=[
            "Attention-based CNN for lung cancer detection",
            "Transformer models for medical image segmentation",
            "Self-supervised learning in radiology",
        ],
        orcid_id="0000-0002-1824-1234",
        scopus_id="57123456789",
        availability=True,
        verified=True,
    ),
    Mentor(
        id=uuid4(),
        name="Dr. Priya Sharma",
        email="psharma@iisc.ac.in",
        affiliation="IISc Bangalore",
        department="Electrical Engineering",
        designation="Associate Professor",
        domain="signal processing",
        research_areas=["speech processing", "audio analysis", "biomedical signal processing"],
        bio="Expert in speech and biomedical signal processing with focus on low-resource Indian languages.",
        h_index=25,
        total_publications=80,
        recent_publications_2yr=8,
        publication_titles=[
            "End-to-end speech recognition for Hindi dialects",
            "EEG signal classification using wavelet transforms",
            "Noise-robust feature extraction for Indian languages",
        ],
        orcid_id="0000-0003-4567-8901",
        scopus_id="57234567890",
        availability=True,
        verified=True,
    ),
    Mentor(
        id=uuid4(),
        name="Dr. Vikram Patel",
        email="vpatel@cse.iitb.ac.in",
        affiliation="IIT Bombay",
        department="Computer Science",
        designation="Professor",
        domain="natural language processing",
        research_areas=["LLMs", "question answering", "information extraction", "machine translation"],
        bio="Working on large language models and their applications in Indian languages.",
        h_index=42,
        total_publications=150,
        recent_publications_2yr=18,
        publication_titles=[
            "IndicBERT: Pre-training for Indian languages",
            "Cross-lingual transfer for low-resource NLP",
            "Legal document summarization using transformers",
        ],
        orcid_id="0000-0001-2345-6789",
        scopus_id="57345678901",
        availability=True,
        verified=True,
    ),
    Mentor(
        id=uuid4(),
        name="Dr. Ananya Gupta",
        email="agupta@nitk.ac.in",
        affiliation="NIT Karnataka",
        department="Electronics & Communication",
        designation="Associate Professor",
        domain="computer vision",
        research_areas=["object detection", "autonomous driving", "video analytics"],
        bio="Researching computer vision for autonomous systems and surveillance.",
        h_index=20,
        total_publications=55,
        recent_publications_2yr=6,
        publication_titles=[
            "Real-time pedestrian detection for Indian traffic",
            "Video anomaly detection in crowded scenes",
        ],
        orcid_id="0000-0002-9876-5432",
        scopus_id="57456789012",
        availability=True,
        verified=True,
    ),
    Mentor(
        id=uuid4(),
        name="Dr. Suresh Kumar",
        email="skumar@curaj.ac.in",
        affiliation="Central University of Rajasthan",
        department="Computer Science",
        designation="Assistant Professor",
        domain="reinforcement learning",
        research_areas=["RL", "robotics", "game theory", "multi-agent systems"],
        bio="Working on reinforcement learning algorithms for robotics and multi-agent coordination.",
        h_index=15,
        total_publications=35,
        recent_publications_2yr=5,
        publication_titles=[
            "Multi-agent RL for traffic signal control",
            "Inverse RL for autonomous navigation",
        ],
        orcid_id="0000-0003-1111-2222",
        scopus_id="57567890123",
        availability=True,
        verified=True,
    ),
    Mentor(
        id=uuid4(),
        name="Dr. Neha Singh",
        email="nsingh@ipr.iitm.ac.in",
        affiliation="IIT Madras",
        department="IP Office / Technology Transfer",
        designation="IP Attorney",
        domain="intellectual property",
        research_areas=["patent drafting", "prior art search", "technology licensing", "IP strategy"],
        bio="Licensed patent agent with 10+ years of experience in drafting and filing patents at IPO India.",
        h_index=8,
        total_publications=20,
        recent_publications_2yr=3,
        publication_titles=[
            "AI-assisted patent prior art search methods",
            "Technology transfer best practices in Indian universities",
        ],
        orcid_id="0000-0004-3333-4444",
        scopus_id="57678901234",
        availability=True,
        verified=True,
    ),
    Mentor(
        id=uuid4(),
        name="Dr. Rajesh Iyer",
        email="riyer@barc.gov.in",
        affiliation="BARC / HBNI",
        department="Nuclear Physics",
        designation="Scientist G",
        domain="physics",
        research_areas=["nuclear physics", "radiation detection", "material science"],
        bio="Senior scientist working on radiation detection systems and nuclear instrumentation.",
        h_index=30,
        total_publications=90,
        recent_publications_2yr=7,
        publication_titles=[
            "Gamma spectroscopy for contraband detection",
            "Advanced scintillator materials for radiation monitoring",
        ],
        orcid_id="0000-0005-5555-6666",
        scopus_id="57789012345",
        availability=False,
        verified=True,
    ),
    Mentor(
        id=uuid4(),
        name="Dr. Kavita Joshi",
        email="kjoshi@cs.du.ac.in",
        affiliation="University of Delhi",
        department="Computer Science",
        designation="Professor",
        domain="data science",
        research_areas=["big data", "data mining", "recommender systems", "social network analysis"],
        bio="Data science researcher focused on recommender systems and social media analytics.",
        h_index=22,
        total_publications=65,
        recent_publications_2yr=9,
        publication_titles=[
            "Graph neural networks for social recommendation",
            "Temporal dynamics in collaborative filtering",
        ],
        orcid_id="0000-0006-7777-8888",
        scopus_id="57890123456",
        availability=True,
        verified=True,
    ),
    Mentor(
        id=uuid4(),
        name="Dr. Aditya Rao",
        email="arao@ds.iitkgp.ac.in",
        affiliation="IIT Kharagpur",
        department="Computer Science & Engineering",
        designation="Assistant Professor",
        domain="generative AI",
        research_areas=["diffusion models", "GANS", "AI for creative arts", "3D generation"],
        bio="Exploring generative models for content creation including images, music, and 3D assets.",
        h_index=18,
        total_publications=40,
        recent_publications_2yr=10,
        publication_titles=[
            "Controllable image generation with diffusion models",
            "Music generation using transformer architectures",
            "Neural radiance fields for 3D scene reconstruction",
        ],
        orcid_id="0000-0007-9999-0000",
        scopus_id="57901234567",
        availability=True,
        verified=True,
    ),
    Mentor(
        id=uuid4(),
        name="Dr. Sunita Reddy",
        email="sreddy@cvr.iith.ac.in",
        affiliation="IIT Hyderabad",
        department="Artificial Intelligence",
        designation="Associate Professor",
        domain="computer vision",
        research_areas=["medical image analysis", "ophthalmic imaging", "deep learning"],
        bio="Developing AI systems for automated diagnosis from retinal and ophthalmic images.",
        h_index=28,
        total_publications=75,
        recent_publications_2yr=11,
        publication_titles=[
            "Deep learning for diabetic retinopathy screening",
            "Multi-modal ophthalmic image fusion",
            "Explainable AI for medical diagnosis",
        ],
        orcid_id="0000-0008-1111-2222",
        scopus_id="58012345678",
        availability=True,
        verified=True,
    ),
]


def save_mentors(mentors: list[Mentor], filepath: str = "data/mentors.json"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump([m.model_dump(mode="json") for m in mentors], f, indent=2, default=str)


def load_mentors(filepath: str = "data/mentors.json") -> list[Mentor]:
    if not os.path.exists(filepath):
        return []
    with open(filepath) as f:
        return [Mentor(**m) for m in json.load(f)]


def load_or_create_mentors() -> list[Mentor]:
    mentors = load_mentors()
    if not mentors:
        mentors = SEED_MENTORS
        save_mentors(mentors)
    return mentors


def compute_and_cache_embeddings(mentors: list[Mentor]):
    texts = [build_mentor_text(m.bio, m.research_areas, m.publication_titles) for m in mentors]
    embeddings = embed_texts(texts)
    for i, m in enumerate(mentors):
        m.embedding = embeddings[i].tolist()
    save_mentors(mentors)


SAMPLE_PROJECT_INPUTS = [
    ProjectInput(
        title="AI-powered early detection of diabetic retinopathy",
        abstract="This project aims to develop a deep learning model to detect diabetic retinopathy from retinal fundus images. We will use convolutional neural networks and attention mechanisms to achieve high accuracy in early-stage detection, making screening accessible in rural India.",
        domain="computer vision",
        goal=ProjectGoal.paper,
        scholar_id=uuid4(),
    ),
    ProjectInput(
        title="Indic language speech-to-text for healthcare",
        abstract="Building an end-to-end speech recognition system for Hindi and other Indian languages specifically optimized for medical transcription in low-resource settings.",
        domain="signal processing",
        goal=ProjectGoal.invention,
        scholar_id=uuid4(),
    ),
    ProjectInput(
        title="Patent drafting: Smart irrigation system using IoT",
        abstract="A novel smart irrigation system combining soil moisture sensors, weather API data, and ML-based predictive scheduling to optimize water usage in Indian agriculture.",
        domain="intellectual property",
        goal=ProjectGoal.patent,
        scholar_id=uuid4(),
    ),
    ProjectInput(
        title="Reinforcement learning for adaptive traffic signal control",
        abstract="Designing a multi-agent reinforcement learning framework for adaptive traffic signal control at busy Indian intersections to reduce congestion and emissions.",
        domain="reinforcement learning",
        goal=ProjectGoal.paper,
        scholar_id=uuid4(),
    ),
    ProjectInput(
        title="Generative AI for creating educational content in regional languages",
        abstract="Using diffusion models and LLMs to automatically generate illustrated educational content (text + images) for K-12 students in Hindi, Tamil, and Marathi.",
        domain="generative AI",
        goal=ProjectGoal.paper,
        scholar_id=uuid4(),
    ),
]


def embed_projects(projects: list[Project]):
    texts = [build_project_text(p.title, p.abstract, p.domain) for p in projects]
    embeddings = embed_texts(texts)
    for i, p in enumerate(projects):
        p.embedding = embeddings[i].tolist()
