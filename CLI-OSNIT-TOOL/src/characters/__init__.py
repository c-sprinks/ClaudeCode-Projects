#!/usr/bin/env python3
"""
Inspector Gadget Characters Module

This module contains implementations of all the beloved Inspector Gadget characters:
- Brain: The intelligent AI coordinator (already implemented in ../ai/brain.py)
- Penny: User interface assistant and data visualization expert
- Chief Quimby: Mission briefings and case management
- M.A.D. Agents: Threat detection and security monitoring

Each character brings their unique personality and capabilities to Inspector-G's
advanced OSINT operations.
"""

from .penny import Penny
from .chief_quimby import ChiefQuimby
from .mad_detection import MADDetection

__all__ = ['Penny', 'ChiefQuimby', 'MADDetection']