from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class SkillLevel(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4

@dataclass
class Employee:
    employee_id: str
    name: str
    role: str
    skills: Dict[str, SkillLevel]
    training_completed: List[str]
    current_projects: List[str]

class HRAgent:
    """Autonomous HR and workforce management agent."""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.employees: Dict[str, Employee] = {}
        self.job_openings: List[Dict[str, Any]] = []
        self.training_programs: Dict[str, List[str]] = {}
        self.skill_gap_analysis: Dict[str, List[str]] = {}
    
    def hire_employee(self, employee: Employee) -> bool:
        """Onboard new employee."""
        if employee.employee_id in self.employees:
            return False
        self.employees[employee.employee_id] = employee
        return True
    
    def recommend_training(self, employee_id: str) -> List[str]:
        """Recommend training programs."""
        if employee_id not in self.employees:
            return []
        return ['Python_Fundamentals', 'ML_101']
    
    def post_job(self, role: str, department: str, required_skills: List[str]) -> str:
        """Post job opening."""
        job_id = f"job_{len(self.job_openings)}"
        self.job_openings.append({
            'job_id': job_id,
            'role': role,
            'department': department,
            'required_skills': required_skills
        })
        return job_id
    
    def get_workforce_report(self) -> Dict[str, Any]:
        """Generate workforce report."""
        return {
            'total_employees': len(self.employees),
            'open_positions': len(self.job_openings)
        }
