#!/usr/bin/env python3
"""
Behavioral Fingerprint Engine for Inspector-G
Revolutionary behavioral DNA analysis for cross-platform user correlation

Like Brain the dog's invisible intelligence, this module creates unique behavioral
signatures that can identify the same person across different platforms with
statistical confidence scoring.
"""

import asyncio
import re
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
import pandas as pd
from textstat import flesch_reading_ease, syllable_count
import logging

from ...ai.neural_engine import NeuralFoundationEngine, BehavioralPattern, CorrelationResult

logger = logging.getLogger(__name__)


class SignatureType(Enum):
    """Types of behavioral signatures"""
    LINGUISTIC = "linguistic"
    TEMPORAL = "temporal"
    INTERACTION = "interaction"
    CONTENT = "content"
    TECHNICAL = "technical"


@dataclass
class LinguisticSignature:
    """Advanced linguistic behavior analysis"""
    vocabulary_complexity: float
    average_sentence_length: float
    punctuation_density: Dict[str, float]
    capitalization_ratio: float
    emoji_usage_pattern: Dict[str, int]
    typo_patterns: List[str]
    common_phrases: List[str]
    reading_level: float
    unique_expressions: List[str]
    grammar_patterns: Dict[str, float]

    def to_vector(self) -> np.ndarray:
        """Convert to numerical vector for ML processing"""
        vector = [
            self.vocabulary_complexity,
            self.average_sentence_length,
            self.capitalization_ratio,
            self.reading_level,
            len(self.emoji_usage_pattern),
            len(self.typo_patterns),
            len(self.common_phrases),
            sum(self.punctuation_density.values())
        ]
        return np.array(vector)


@dataclass
class TemporalSignature:
    """Advanced temporal behavior analysis"""
    activity_hours: Dict[int, float]  # Hour of day -> activity ratio
    weekly_pattern: Dict[str, float]  # Day of week -> activity ratio
    posting_frequency: float  # Posts per day average
    burst_patterns: List[Tuple[datetime, int]]  # Time, burst size
    response_timing: List[float]  # Response delays in minutes
    timezone_inference: Optional[str]
    sleep_schedule: Tuple[int, int]  # Likely sleep hours
    work_schedule_indicators: Dict[str, float]

    def to_vector(self) -> np.ndarray:
        """Convert to numerical vector for ML processing"""
        vector = [
            self.posting_frequency,
            max(self.activity_hours.values()) if self.activity_hours else 0,
            statistics.mean(self.response_timing) if self.response_timing else 0,
            len(self.burst_patterns),
            self.sleep_schedule[1] - self.sleep_schedule[0] if self.sleep_schedule else 8
        ]
        # Add hourly activity distribution (24 values)
        hourly_dist = [self.activity_hours.get(h, 0) for h in range(24)]
        vector.extend(hourly_dist)
        return np.array(vector)


@dataclass
class InteractionSignature:
    """Social interaction behavior analysis"""
    interaction_style: Dict[str, float]  # Like ratios, comment styles
    social_network_size: int
    engagement_patterns: Dict[str, float]
    conversation_initiation_rate: float
    response_patterns: Dict[str, float]
    conflict_avoidance_score: float
    humor_usage_indicators: List[str]
    formality_level: float

    def to_vector(self) -> np.ndarray:
        """Convert to numerical vector for ML processing"""
        vector = [
            self.social_network_size,
            self.conversation_initiation_rate,
            self.conflict_avoidance_score,
            self.formality_level,
            len(self.humor_usage_indicators)
        ]
        # Add engagement pattern values
        vector.extend(list(self.engagement_patterns.values())[:5])  # Limit to 5
        return np.array(vector)


@dataclass
class ContentSignature:
    """Content preference and topical analysis"""
    topic_distribution: Dict[str, float]
    interest_keywords: List[str]
    content_type_preferences: Dict[str, float]  # Text, images, links, etc.
    sharing_behavior: Dict[str, float]
    original_vs_shared_ratio: float
    expertise_indicators: Dict[str, float]
    personal_vs_professional_ratio: float

    def to_vector(self) -> np.ndarray:
        """Convert to numerical vector for ML processing"""
        vector = [
            self.original_vs_shared_ratio,
            self.personal_vs_professional_ratio,
            len(self.interest_keywords),
            max(self.topic_distribution.values()) if self.topic_distribution else 0
        ]
        # Add top content type preferences
        content_prefs = list(self.content_type_preferences.values())[:5]
        vector.extend(content_prefs)
        return np.array(vector)


@dataclass
class TechnicalSignature:
    """Technical behavior and device patterns"""
    device_indicators: List[str]
    browser_patterns: List[str]
    posting_platforms: Dict[str, float]
    image_metadata_patterns: Dict[str, Any]
    url_sharing_patterns: Dict[str, int]
    technical_sophistication: float
    security_awareness_indicators: List[str]

    def to_vector(self) -> np.ndarray:
        """Convert to numerical vector for ML processing"""
        vector = [
            len(self.device_indicators),
            len(self.browser_patterns),
            self.technical_sophistication,
            len(self.security_awareness_indicators)
        ]
        # Add platform distribution
        platform_dist = list(self.posting_platforms.values())[:5]
        vector.extend(platform_dist)
        return np.array(vector)


@dataclass
class BehavioralDNA:
    """Complete behavioral fingerprint - like DNA but for digital behavior"""
    username: str
    platform: str
    analysis_date: datetime
    confidence_score: float

    # Core signature components
    linguistic: LinguisticSignature
    temporal: TemporalSignature
    interaction: InteractionSignature
    content: ContentSignature
    technical: TechnicalSignature

    # Composite analysis
    uniqueness_score: float  # How unique this behavior pattern is
    consistency_score: float  # How consistent the patterns are

    def get_composite_vector(self) -> np.ndarray:
        """Get complete behavioral vector for ML correlation"""
        vectors = [
            self.linguistic.to_vector(),
            self.temporal.to_vector(),
            self.interaction.to_vector(),
            self.content.to_vector(),
            self.technical.to_vector()
        ]

        # Pad vectors to same length and concatenate
        max_len = max(len(v) for v in vectors)
        padded_vectors = []
        for v in vectors:
            if len(v) < max_len:
                padded = np.pad(v, (0, max_len - len(v)), 'constant')
                padded_vectors.append(padded)
            else:
                padded_vectors.append(v)

        return np.concatenate(padded_vectors)


class BehavioralFingerprint:
    """
    Revolutionary behavioral fingerprinting system for Inspector-G

    Creates unique "behavioral DNA" that can identify the same person across
    platforms with statistical confidence. Like Brain the dog's pattern
    recognition, this system sees patterns that are invisible to others.
    """

    def __init__(self, neural_engine: Optional[NeuralFoundationEngine] = None):
        self.neural_engine = neural_engine or NeuralFoundationEngine()
        self.correlation_threshold = 0.75  # Minimum confidence for correlation

        # Pre-compiled regex patterns for efficiency
        self.emoji_pattern = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+')
        self.url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        self.mention_pattern = re.compile(r'@[\w_]+')
        self.hashtag_pattern = re.compile(r'#[\w_]+')

    async def generate_behavioral_fingerprint(
        self,
        username: str,
        platform: str,
        data: Dict[str, Any]
    ) -> BehavioralDNA:
        """
        Generate complete behavioral DNA for a user on a platform

        Args:
            username: Target username
            platform: Platform name (twitter, github, linkedin, etc.)
            data: Platform-specific data (posts, comments, metadata)

        Returns:
            Complete behavioral DNA profile
        """
        logger.info(f"🧬 Generating behavioral DNA for {username} on {platform}")

        try:
            # Extract different data types
            text_data = self._extract_text_data(data)
            temporal_data = self._extract_temporal_data(data)
            interaction_data = self._extract_interaction_data(data)
            content_data = self._extract_content_data(data)
            technical_data = self._extract_technical_data(data)

            # Generate signatures in parallel for efficiency
            tasks = [
                self._generate_linguistic_signature(text_data),
                self._generate_temporal_signature(temporal_data),
                self._generate_interaction_signature(interaction_data),
                self._generate_content_signature(content_data),
                self._generate_technical_signature(technical_data)
            ]

            signatures = await asyncio.gather(*tasks)

            # Calculate composite scores
            uniqueness_score = await self._calculate_uniqueness_score(signatures)
            consistency_score = await self._calculate_consistency_score(signatures)
            confidence_score = await self._calculate_confidence_score(
                text_data, temporal_data, signatures
            )

            behavioral_dna = BehavioralDNA(
                username=username,
                platform=platform,
                analysis_date=datetime.now(),
                confidence_score=confidence_score,
                linguistic=signatures[0],
                temporal=signatures[1],
                interaction=signatures[2],
                content=signatures[3],
                technical=signatures[4],
                uniqueness_score=uniqueness_score,
                consistency_score=consistency_score
            )

            logger.info(f"✅ Behavioral DNA generated with {confidence_score:.1%} confidence")
            return behavioral_dna

        except Exception as e:
            logger.error(f"❌ Error generating behavioral fingerprint: {e}")
            raise

    async def correlate_behavioral_dna(
        self,
        dna1: BehavioralDNA,
        dna2: BehavioralDNA
    ) -> CorrelationResult:
        """
        Correlate two behavioral DNA profiles to determine if same person

        Uses advanced AI correlation across multiple behavioral dimensions
        with statistical confidence scoring.
        """
        logger.info(f"🔬 Correlating behavioral DNA: {dna1.username}@{dna1.platform} vs {dna2.username}@{dna2.platform}")

        try:
            # Get behavioral vectors
            vector1 = dna1.get_composite_vector()
            vector2 = dna2.get_composite_vector()

            # Calculate correlations across different signature types
            correlations = {
                'linguistic': await self._correlate_signatures(dna1.linguistic, dna2.linguistic),
                'temporal': await self._correlate_signatures(dna1.temporal, dna2.temporal),
                'interaction': await self._correlate_signatures(dna1.interaction, dna2.interaction),
                'content': await self._correlate_signatures(dna1.content, dna2.content),
                'technical': await self._correlate_signatures(dna1.technical, dna2.technical)
            }

            # Use neural engine for advanced correlation
            neural_correlation = await self.neural_engine.correlate_behavioral_patterns(
                vector1, vector2, correlations
            )

            # Calculate weighted confidence score
            weights = {
                'linguistic': 0.25,
                'temporal': 0.20,
                'interaction': 0.20,
                'content': 0.15,
                'technical': 0.20
            }

            weighted_score = sum(
                correlations[sig_type] * weight
                for sig_type, weight in weights.items()
            )

            # Combine with neural correlation
            final_confidence = (weighted_score * 0.7) + (neural_correlation * 0.3)

            # Determine if correlation is significant
            is_match = final_confidence >= self.correlation_threshold

            evidence_points = self._generate_evidence_points(correlations, dna1, dna2)

            result = CorrelationResult(
                confidence_score=final_confidence,
                is_likely_match=is_match,
                correlation_breakdown=correlations,
                evidence_points=evidence_points,
                comparison_data={
                    'profiles': f"{dna1.username}@{dna1.platform} ↔ {dna2.username}@{dna2.platform}",
                    'analysis_method': 'behavioral_dna_correlation',
                    'neural_correlation': neural_correlation,
                    'weighted_score': weighted_score
                }
            )

            logger.info(f"🎯 Correlation complete: {final_confidence:.1%} confidence ({'MATCH' if is_match else 'NO MATCH'})")
            return result

        except Exception as e:
            logger.error(f"❌ Error correlating behavioral DNA: {e}")
            raise

    async def _generate_linguistic_signature(self, text_data: List[str]) -> LinguisticSignature:
        """Generate advanced linguistic behavioral signature"""
        if not text_data:
            return LinguisticSignature(
                vocabulary_complexity=0, average_sentence_length=0,
                punctuation_density={}, capitalization_ratio=0,
                emoji_usage_pattern={}, typo_patterns=[],
                common_phrases=[], reading_level=0,
                unique_expressions=[], grammar_patterns={}
            )

        # Combine all text
        combined_text = " ".join(text_data)

        # Vocabulary complexity (unique words / total words)
        words = re.findall(r'\b\w+\b', combined_text.lower())
        vocab_complexity = len(set(words)) / max(len(words), 1)

        # Sentence analysis
        sentences = re.split(r'[.!?]+', combined_text)
        avg_sentence_length = statistics.mean([len(s.split()) for s in sentences if s.strip()])

        # Punctuation analysis
        punctuation_chars = "!@#$%^&*(),.?;:'\""
        total_chars = len(combined_text)
        punctuation_density = {
            char: combined_text.count(char) / max(total_chars, 1)
            for char in punctuation_chars
        }

        # Capitalization analysis
        letters = [c for c in combined_text if c.isalpha()]
        cap_ratio = sum(1 for c in letters if c.isupper()) / max(len(letters), 1)

        # Emoji pattern analysis
        emojis = self.emoji_pattern.findall(combined_text)
        emoji_usage = Counter(emojis)

        # Typo pattern detection (simple heuristic)
        typo_patterns = self._detect_typo_patterns(words)

        # Common phrases extraction
        common_phrases = self._extract_common_phrases(text_data)

        # Reading level
        reading_level = flesch_reading_ease(combined_text) if combined_text else 0

        # Unique expressions
        unique_expressions = self._find_unique_expressions(text_data)

        # Grammar patterns (simplified)
        grammar_patterns = self._analyze_grammar_patterns(text_data)

        return LinguisticSignature(
            vocabulary_complexity=vocab_complexity,
            average_sentence_length=avg_sentence_length,
            punctuation_density=punctuation_density,
            capitalization_ratio=cap_ratio,
            emoji_usage_pattern=dict(emoji_usage),
            typo_patterns=typo_patterns,
            common_phrases=common_phrases,
            reading_level=reading_level,
            unique_expressions=unique_expressions,
            grammar_patterns=grammar_patterns
        )

    async def _generate_temporal_signature(self, temporal_data: List[Dict]) -> TemporalSignature:
        """Generate temporal behavioral signature"""
        if not temporal_data:
            return TemporalSignature(
                activity_hours={}, weekly_pattern={},
                posting_frequency=0, burst_patterns=[],
                response_timing=[], timezone_inference=None,
                sleep_schedule=(0, 8), work_schedule_indicators={}
            )

        # Extract timestamps
        timestamps = []
        for item in temporal_data:
            if 'timestamp' in item:
                timestamps.append(datetime.fromisoformat(item['timestamp'].replace('Z', '+00:00')))

        if not timestamps:
            return TemporalSignature(
                activity_hours={}, weekly_pattern={},
                posting_frequency=0, burst_patterns=[],
                response_timing=[], timezone_inference=None,
                sleep_schedule=(0, 8), work_schedule_indicators={}
            )

        # Activity hours analysis
        activity_hours = defaultdict(int)
        for ts in timestamps:
            activity_hours[ts.hour] += 1

        # Normalize to ratios
        total_posts = len(timestamps)
        activity_hours = {hour: count/total_posts for hour, count in activity_hours.items()}

        # Weekly pattern analysis
        weekly_pattern = defaultdict(int)
        for ts in timestamps:
            weekly_pattern[ts.strftime('%A')] += 1
        weekly_pattern = {day: count/total_posts for day, count in weekly_pattern.items()}

        # Posting frequency (posts per day)
        if len(timestamps) > 1:
            time_span = (max(timestamps) - min(timestamps)).days or 1
            posting_frequency = total_posts / time_span
        else:
            posting_frequency = 1

        # Burst pattern detection
        burst_patterns = self._detect_burst_patterns(timestamps)

        # Response timing analysis (simplified)
        response_timing = self._analyze_response_timing(temporal_data)

        # Timezone inference
        timezone_inference = self._infer_timezone(activity_hours)

        # Sleep schedule inference
        sleep_schedule = self._infer_sleep_schedule(activity_hours)

        # Work schedule indicators
        work_schedule_indicators = self._analyze_work_schedule(activity_hours, weekly_pattern)

        return TemporalSignature(
            activity_hours=activity_hours,
            weekly_pattern=weekly_pattern,
            posting_frequency=posting_frequency,
            burst_patterns=burst_patterns,
            response_timing=response_timing,
            timezone_inference=timezone_inference,
            sleep_schedule=sleep_schedule,
            work_schedule_indicators=work_schedule_indicators
        )

    async def _generate_interaction_signature(self, interaction_data: Dict) -> InteractionSignature:
        """Generate social interaction behavioral signature"""
        # Extract interaction metrics
        likes_given = interaction_data.get('likes_given', 0)
        comments_made = interaction_data.get('comments_made', 0)
        shares_made = interaction_data.get('shares_made', 0)
        followers_count = interaction_data.get('followers', 0)
        following_count = interaction_data.get('following', 0)

        # Calculate interaction style ratios
        total_interactions = likes_given + comments_made + shares_made
        interaction_style = {
            'like_ratio': likes_given / max(total_interactions, 1),
            'comment_ratio': comments_made / max(total_interactions, 1),
            'share_ratio': shares_made / max(total_interactions, 1)
        }

        # Social network size estimation
        social_network_size = followers_count + following_count

        # Engagement patterns
        engagement_patterns = {
            'follower_to_following_ratio': followers_count / max(following_count, 1),
            'interaction_to_follower_ratio': total_interactions / max(followers_count, 1)
        }

        # Simplified metrics (would be more complex with real data)
        conversation_initiation_rate = comments_made / max(total_interactions, 1)
        conflict_avoidance_score = 0.5  # Would analyze sentiment of interactions
        formality_level = 0.5  # Would analyze language formality

        return InteractionSignature(
            interaction_style=interaction_style,
            social_network_size=social_network_size,
            engagement_patterns=engagement_patterns,
            conversation_initiation_rate=conversation_initiation_rate,
            response_patterns={},
            conflict_avoidance_score=conflict_avoidance_score,
            humor_usage_indicators=[],
            formality_level=formality_level
        )

    async def _generate_content_signature(self, content_data: Dict) -> ContentSignature:
        """Generate content preference behavioral signature"""
        # Extract content metrics
        posts = content_data.get('posts', [])
        shared_content = content_data.get('shared_content', [])

        # Topic distribution (simplified)
        topic_distribution = self._analyze_topic_distribution(posts)

        # Content type preferences
        content_types = defaultdict(int)
        for post in posts:
            if 'images' in post:
                content_types['image'] += len(post['images'])
            if 'links' in post:
                content_types['link'] += len(post['links'])
            if 'text' in post and post['text']:
                content_types['text'] += 1

        total_content = sum(content_types.values())
        content_type_preferences = {
            ctype: count / max(total_content, 1)
            for ctype, count in content_types.items()
        }

        # Original vs shared ratio
        original_posts = len(posts)
        shared_posts = len(shared_content)
        original_vs_shared_ratio = original_posts / max(original_posts + shared_posts, 1)

        return ContentSignature(
            topic_distribution=topic_distribution,
            interest_keywords=[],
            content_type_preferences=content_type_preferences,
            sharing_behavior={},
            original_vs_shared_ratio=original_vs_shared_ratio,
            expertise_indicators={},
            personal_vs_professional_ratio=0.5
        )

    async def _generate_technical_signature(self, technical_data: Dict) -> TechnicalSignature:
        """Generate technical behavioral signature"""
        # Extract technical indicators
        device_indicators = technical_data.get('device_indicators', [])
        browser_patterns = technical_data.get('browser_patterns', [])
        platforms_used = technical_data.get('platforms', {})

        # Calculate technical sophistication (simplified)
        tech_indicators = len(device_indicators) + len(browser_patterns)
        technical_sophistication = min(tech_indicators / 10, 1.0)  # Normalize to 0-1

        return TechnicalSignature(
            device_indicators=device_indicators,
            browser_patterns=browser_patterns,
            posting_platforms=platforms_used,
            image_metadata_patterns={},
            url_sharing_patterns={},
            technical_sophistication=technical_sophistication,
            security_awareness_indicators=[]
        )

    def _extract_text_data(self, data: Dict[str, Any]) -> List[str]:
        """Extract text content from platform data"""
        text_data = []

        # Extract from posts
        posts = data.get('posts', [])
        for post in posts:
            if isinstance(post, dict) and 'text' in post:
                text_data.append(post['text'])
            elif isinstance(post, str):
                text_data.append(post)

        # Extract from comments
        comments = data.get('comments', [])
        for comment in comments:
            if isinstance(comment, dict) and 'text' in comment:
                text_data.append(comment['text'])
            elif isinstance(comment, str):
                text_data.append(comment)

        # Extract from bio/description
        if 'bio' in data:
            text_data.append(data['bio'])
        if 'description' in data:
            text_data.append(data['description'])

        return [text for text in text_data if text and isinstance(text, str)]

    def _extract_temporal_data(self, data: Dict[str, Any]) -> List[Dict]:
        """Extract temporal data from platform data"""
        temporal_data = []

        # Extract timestamps from posts
        posts = data.get('posts', [])
        for post in posts:
            if isinstance(post, dict) and 'timestamp' in post:
                temporal_data.append({
                    'timestamp': post['timestamp'],
                    'type': 'post',
                    'metadata': post
                })

        # Extract timestamps from comments
        comments = data.get('comments', [])
        for comment in comments:
            if isinstance(comment, dict) and 'timestamp' in comment:
                temporal_data.append({
                    'timestamp': comment['timestamp'],
                    'type': 'comment',
                    'metadata': comment
                })

        return temporal_data

    def _extract_interaction_data(self, data: Dict[str, Any]) -> Dict:
        """Extract interaction data from platform data"""
        return {
            'likes_given': data.get('likes_given', 0),
            'comments_made': data.get('comments_made', 0),
            'shares_made': data.get('shares_made', 0),
            'followers': data.get('followers', 0),
            'following': data.get('following', 0),
            'interactions': data.get('interactions', [])
        }

    def _extract_content_data(self, data: Dict[str, Any]) -> Dict:
        """Extract content data from platform data"""
        return {
            'posts': data.get('posts', []),
            'shared_content': data.get('shared_content', []),
            'media': data.get('media', []),
            'links': data.get('links', [])
        }

    def _extract_technical_data(self, data: Dict[str, Any]) -> Dict:
        """Extract technical data from platform data"""
        return {
            'device_indicators': data.get('device_indicators', []),
            'browser_patterns': data.get('browser_patterns', []),
            'platforms': data.get('platforms', {}),
            'metadata': data.get('metadata', {})
        }

    async def _correlate_signatures(self, sig1: Any, sig2: Any) -> float:
        """Correlate two behavioral signatures using advanced techniques"""
        try:
            # Convert signatures to vectors
            vec1 = sig1.to_vector()
            vec2 = sig2.to_vector()

            # Ensure vectors are same length
            min_len = min(len(vec1), len(vec2))
            vec1 = vec1[:min_len]
            vec2 = vec2[:min_len]

            # Calculate correlation coefficient
            if len(vec1) > 1 and np.std(vec1) > 0 and np.std(vec2) > 0:
                correlation = np.corrcoef(vec1, vec2)[0, 1]
                # Handle NaN values
                if np.isnan(correlation):
                    correlation = 0
                # Convert to positive correlation (absolute value)
                return abs(correlation)
            else:
                return 0
        except Exception as e:
            logger.warning(f"Error correlating signatures: {e}")
            return 0

    # Helper methods for signature generation
    def _detect_typo_patterns(self, words: List[str]) -> List[str]:
        """Detect common typo patterns"""
        # Simple typo detection (could be enhanced with ML)
        potential_typos = []
        for word in words:
            if len(word) > 3:
                # Check for doubled letters
                if re.search(r'(.)\1{2,}', word):
                    potential_typos.append(word)
                # Check for common substitutions
                if re.search(r'teh|hte|adn|nad', word):
                    potential_typos.append(word)
        return list(set(potential_typos))

    def _extract_common_phrases(self, text_data: List[str]) -> List[str]:
        """Extract commonly used phrases"""
        # Simple ngram extraction
        phrases = []
        for text in text_data:
            words = text.lower().split()
            # Extract 2-grams and 3-grams
            for i in range(len(words) - 1):
                phrases.append(' '.join(words[i:i+2]))
            for i in range(len(words) - 2):
                phrases.append(' '.join(words[i:i+3]))

        # Return most common phrases
        phrase_counts = Counter(phrases)
        return [phrase for phrase, count in phrase_counts.most_common(10) if count > 1]

    def _find_unique_expressions(self, text_data: List[str]) -> List[str]:
        """Find unique expressions and catchphrases"""
        # Look for repeated unique expressions
        expressions = []
        for text in text_data:
            # Find expressions in quotes
            quoted = re.findall(r'"([^"]*)"', text)
            expressions.extend(quoted)
            # Find expressions with special patterns
            special = re.findall(r'\b\w+(?:ly|ish|ness)\b', text.lower())
            expressions.extend(special)

        # Return expressions that appear multiple times
        expr_counts = Counter(expressions)
        return [expr for expr, count in expr_counts.most_common(5) if count > 1]

    def _analyze_grammar_patterns(self, text_data: List[str]) -> Dict[str, float]:
        """Analyze grammar and sentence structure patterns"""
        patterns = defaultdict(int)
        total_sentences = 0

        for text in text_data:
            sentences = re.split(r'[.!?]+', text)
            for sentence in sentences:
                if sentence.strip():
                    total_sentences += 1
                    # Check for question vs statement
                    if '?' in sentence:
                        patterns['questions'] += 1
                    elif '!' in sentence:
                        patterns['exclamations'] += 1
                    else:
                        patterns['statements'] += 1

                    # Check for passive voice (simplified)
                    if re.search(r'\b(was|were|been|being)\s+\w+ed\b', sentence):
                        patterns['passive_voice'] += 1

        # Convert to ratios
        return {pattern: count / max(total_sentences, 1) for pattern, count in patterns.items()}

    def _detect_burst_patterns(self, timestamps: List[datetime]) -> List[Tuple[datetime, int]]:
        """Detect burst patterns in posting activity"""
        if len(timestamps) < 2:
            return []

        # Sort timestamps
        sorted_timestamps = sorted(timestamps)
        bursts = []

        # Look for periods with high activity (multiple posts within 1 hour)
        current_burst = []
        for i, ts in enumerate(sorted_timestamps):
            if current_burst and (ts - current_burst[-1]).total_seconds() > 3600:  # 1 hour
                if len(current_burst) >= 3:  # At least 3 posts for a burst
                    bursts.append((current_burst[0], len(current_burst)))
                current_burst = [ts]
            else:
                current_burst.append(ts)

        # Check final burst
        if len(current_burst) >= 3:
            bursts.append((current_burst[0], len(current_burst)))

        return bursts

    def _analyze_response_timing(self, temporal_data: List[Dict]) -> List[float]:
        """Analyze response timing patterns"""
        # Simplified: would need conversation thread data for real analysis
        response_times = []

        # For now, simulate some response timing analysis
        for item in temporal_data:
            if item.get('type') == 'comment':
                # Simulate response time in minutes
                response_times.append(30.0)  # Placeholder

        return response_times

    def _infer_timezone(self, activity_hours: Dict[int, float]) -> Optional[str]:
        """Infer timezone from activity patterns"""
        if not activity_hours:
            return None

        # Find peak activity hour
        peak_hour = max(activity_hours, key=activity_hours.get)

        # Simple timezone inference based on peak activity
        # (would be more sophisticated with real data)
        if 9 <= peak_hour <= 17:
            return "US/Eastern"  # Business hours
        elif 18 <= peak_hour <= 23:
            return "US/Pacific"  # Evening activity
        else:
            return "UTC"  # Default

    def _infer_sleep_schedule(self, activity_hours: Dict[int, float]) -> Tuple[int, int]:
        """Infer likely sleep schedule from activity patterns"""
        if not activity_hours:
            return (0, 8)

        # Find hours with lowest activity (likely sleep time)
        sorted_hours = sorted(activity_hours.items(), key=lambda x: x[1])

        # Find consecutive low-activity hours
        low_activity_hours = [hour for hour, activity in sorted_hours[:8]]

        if low_activity_hours:
            sleep_start = min(low_activity_hours)
            sleep_end = (sleep_start + 8) % 24
            return (sleep_start, sleep_end)

        return (0, 8)  # Default 8-hour sleep

    def _analyze_work_schedule(self, activity_hours: Dict, weekly_pattern: Dict) -> Dict[str, float]:
        """Analyze work schedule indicators"""
        indicators = {}

        # Business hours activity
        business_hours = [9, 10, 11, 12, 13, 14, 15, 16, 17]
        business_activity = sum(activity_hours.get(hour, 0) for hour in business_hours)
        indicators['business_hours_activity'] = business_activity

        # Weekday vs weekend activity
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        weekends = ['Saturday', 'Sunday']

        weekday_activity = sum(weekly_pattern.get(day, 0) for day in weekdays)
        weekend_activity = sum(weekly_pattern.get(day, 0) for day in weekends)

        if weekend_activity > 0:
            indicators['weekday_to_weekend_ratio'] = weekday_activity / weekend_activity
        else:
            indicators['weekday_to_weekend_ratio'] = weekday_activity

        return indicators

    def _analyze_topic_distribution(self, posts: List[Dict]) -> Dict[str, float]:
        """Analyze topic distribution in posts"""
        # Simplified topic analysis
        topics = defaultdict(int)
        total_posts = len(posts)

        # Keywords for different topics
        topic_keywords = {
            'technology': ['tech', 'software', 'code', 'programming', 'computer'],
            'business': ['business', 'work', 'career', 'professional', 'company'],
            'personal': ['family', 'friends', 'personal', 'life', 'love'],
            'sports': ['sports', 'game', 'team', 'player', 'match'],
            'politics': ['politics', 'government', 'election', 'policy', 'vote']
        }

        for post in posts:
            text = post.get('text', '').lower() if isinstance(post, dict) else str(post).lower()
            for topic, keywords in topic_keywords.items():
                if any(keyword in text for keyword in keywords):
                    topics[topic] += 1

        # Convert to ratios
        return {topic: count / max(total_posts, 1) for topic, count in topics.items()}

    async def _calculate_uniqueness_score(self, signatures: List) -> float:
        """Calculate how unique this behavioral pattern is"""
        # Simplified uniqueness calculation
        # Would compare against database of known patterns in real implementation
        return 0.8  # Placeholder

    async def _calculate_consistency_score(self, signatures: List) -> float:
        """Calculate how consistent the behavioral patterns are"""
        # Simplified consistency calculation
        # Would analyze variance across different signature components
        return 0.7  # Placeholder

    async def _calculate_confidence_score(
        self,
        text_data: List[str],
        temporal_data: List[Dict],
        signatures: List
    ) -> float:
        """Calculate overall confidence score for the behavioral DNA"""
        factors = []

        # Data quantity factor
        data_quantity = len(text_data) + len(temporal_data)
        quantity_factor = min(data_quantity / 100, 1.0)  # Normalize to 0-1
        factors.append(quantity_factor)

        # Data quality factor (presence of different signature types)
        quality_factor = len([sig for sig in signatures if sig is not None]) / len(signatures)
        factors.append(quality_factor)

        # Temporal span factor (more data over time = higher confidence)
        if temporal_data:
            timestamps = [item.get('timestamp') for item in temporal_data if item.get('timestamp')]
            if len(timestamps) > 1:
                time_span = (max(timestamps) - min(timestamps)) if len(timestamps) > 1 else timedelta(days=1)
                span_factor = min(time_span.days / 30, 1.0)  # 30 days = max factor
                factors.append(span_factor)

        # Return average of all factors
        return statistics.mean(factors) if factors else 0.5

    def _generate_evidence_points(
        self,
        correlations: Dict[str, float],
        dna1: BehavioralDNA,
        dna2: BehavioralDNA
    ) -> List[str]:
        """Generate human-readable evidence points for the correlation"""
        evidence = []

        # Add evidence based on correlation strengths
        for sig_type, correlation in correlations.items():
            if correlation > 0.8:
                evidence.append(f"Strong {sig_type} pattern match ({correlation:.1%})")
            elif correlation > 0.6:
                evidence.append(f"Moderate {sig_type} pattern similarity ({correlation:.1%})")

        # Add specific behavioral evidence
        if correlations.get('temporal', 0) > 0.7:
            evidence.append("Similar activity timing patterns suggest same timezone/schedule")

        if correlations.get('linguistic', 0) > 0.7:
            evidence.append("Writing style and vocabulary patterns are highly similar")

        if correlations.get('interaction', 0) > 0.7:
            evidence.append("Social interaction patterns match across platforms")

        return evidence