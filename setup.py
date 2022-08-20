#!/usr/bin/env python3
from setuptools import setup

# skill_id=package_name:SkillClass
PLUGIN_ENTRY_POINT = 'skill-omeleto.jarbasai=skill_omeleto:OmeletoSkill'

setup(
    # this is the package name that goes on pip
    name='ovos-skill-omeleto',
    version='0.0.1',
    description='ovos omeleto skill plugin',
    url='https://github.com/JarbasSkills/skill-omeleto',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    package_dir={"skill_omeleto": ""},
    package_data={'skill_omeleto': ['locale/*', 'ui/*']},
    packages=['skill_omeleto'],
    include_package_data=True,
    install_requires=["ovos_workshop>=0.0.5a1", "youtube_archivist~=0.0.3"],
    keywords='ovos skill plugin',
    entry_points={'ovos.plugin.skill': PLUGIN_ENTRY_POINT}
)
