"""
Utility functions for CodeAlpha_SocialMedia.

Currently contains:
- YouTube Data API v3 search helper
"""

import requests
from django.conf import settings


# ─────────────────────────────────────────────────────────
# YOUTUBE SEARCH FUNCTION
# ─────────────────────────────────────────────────────────
def search_youtube_videos(query, max_results=8):
    """
    YouTube-la videos search pannum (Data API v3 use panni).
    
    Args:
        query (str): Search term (e.g., "KGF trailer")
        max_results (int): Number of results (default 8, max 50)
    
    Returns:
        list: List of dicts, each with:
            - video_id
            - title
            - thumbnail
            - channel
        Returns empty list on error.
    """
    
    # ─────────────────────────────────────────────────
    # API KEY CHECK
    # ─────────────────────────────────────────────────
    api_key = getattr(settings, 'YOUTUBE_API_KEY', None)
    if not api_key:
        print("[YouTube API] ERROR: API key not found in settings")
        return []
    
    # ─────────────────────────────────────────────────
    # API REQUEST PARAMS
    # ─────────────────────────────────────────────────
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': max_results,
        'key': api_key,
        'videoEmbeddable': 'true',   # Embeddable videos mattum
        'safeSearch': 'moderate',     # Safe content
    }
    
    # ─────────────────────────────────────────────────
    # API CALL
    # ─────────────────────────────────────────────────
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()   # Raise error for 4xx, 5xx
        data = response.json()
    
    except requests.exceptions.Timeout:
        print("[YouTube API] ERROR: Request timeout")
        return []
    
    except requests.exceptions.RequestException as e:
        print(f"[YouTube API] ERROR: {e}")
        return []
    
    except ValueError:
        print("[YouTube API] ERROR: Invalid JSON response")
        return []
    
    # ─────────────────────────────────────────────────
    # PARSE RESULTS
    # ─────────────────────────────────────────────────
    results = []
    items = data.get('items', [])
    
    for item in items:
        # Video ID (illa-na skip)
        video_id = item.get('id', {}).get('videoId')
        if not video_id:
            continue
        
        snippet = item.get('snippet', {})
        
        # Thumbnail (best quality available)
        thumbnails = snippet.get('thumbnails', {})
        thumbnail = (
            thumbnails.get('high', {}).get('url') or
            thumbnails.get('medium', {}).get('url') or
            thumbnails.get('default', {}).get('url') or
            ''
        )
        
        results.append({
            'video_id': video_id,
            'title': snippet.get('title', 'Untitled'),
            'thumbnail': thumbnail,
            'channel': snippet.get('channelTitle', 'Unknown'),
        })
    
    return results


# ─────────────────────────────────────────────────────────
# YOUTUBE VIDEO ID VALIDATOR
# ─────────────────────────────────────────────────────────
def is_valid_youtube_id(video_id):
    """
    YouTube video ID valid-ah nu check pannum.
    Valid IDs: 11 characters, alphanumeric + _ + -
    """
    if not video_id:
        return False
    if not isinstance(video_id, str):
        return False
    if len(video_id) != 11:
        return False
    return all(c.isalnum() or c in '-_' for c in video_id)