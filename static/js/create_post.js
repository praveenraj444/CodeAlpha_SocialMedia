/* ───────────────────────────────────────── */
/* CREATE POST — YouTube Search AJAX */
/* ───────────────────────────────────────── */

document.addEventListener('DOMContentLoaded', function () {

    const searchInput = document.getElementById('ytSearchInput');
    const searchBtn = document.getElementById('ytSearchBtn');
    const resultsDiv = document.getElementById('ytResults');
    const loadingDiv = document.getElementById('ytLoading');
    const errorDiv = document.getElementById('ytError');
    const selectedDiv = document.getElementById('ytSelected');
    const selectedThumb = document.getElementById('ytSelectedThumb');
    const selectedTitle = document.getElementById('ytSelectedTitle');
    const removeBtn = document.getElementById('ytRemoveBtn');

    const hiddenVideoId = document.getElementById('id_youtube_video_id');
    const hiddenTitle = document.getElementById('id_youtube_title');
    const hiddenThumb = document.getElementById('id_youtube_thumbnail');

    // ─────────────────────────────────────────
    // SEARCH BUTTON
    // ─────────────────────────────────────────
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            performSearch();
        }
    });

    function performSearch() {
        const query = searchInput.value.trim();
        if (!query) {
            showError('Please enter a search term.');
            return;
        }

        // Reset UI
        errorDiv.classList.add('d-none');
        resultsDiv.innerHTML = '';
        loadingDiv.classList.remove('d-none');

        fetch(`/youtube-search/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                loadingDiv.classList.add('d-none');

                if (data.error) {
                    showError(data.error);
                    return;
                }

                if (!data.results || data.results.length === 0) {
                    showError('No results found. Try a different search.');
                    return;
                }

                renderResults(data.results);
            })
            .catch(err => {
                loadingDiv.classList.add('d-none');
                showError('Network error. Please try again.');
                console.error(err);
            });
    }

    function renderResults(results) {
        resultsDiv.innerHTML = '';

        results.forEach(video => {
            const item = document.createElement('div');
            item.className = 'yt-result-item';
            item.innerHTML = `
                <img src="${video.thumbnail}" class="yt-result-thumb" alt="thumb">
                <div class="yt-result-info">
                    <div class="yt-result-title">${escapeHtml(video.title)}</div>
                    <div class="yt-result-channel">${escapeHtml(video.channel)}</div>
                </div>
            `;
            item.addEventListener('click', () => selectVideo(video, item));
            resultsDiv.appendChild(item);
        });
    }

    function selectVideo(video, element) {
        // Highlight selected
        document.querySelectorAll('.yt-result-item').forEach(el => el.classList.remove('selected'));
        element.classList.add('selected');

        // Fill hidden fields
        hiddenVideoId.value = video.video_id;
        hiddenTitle.value = video.title;
        hiddenThumb.value = video.thumbnail;

        // Show preview
        selectedThumb.src = video.thumbnail;
        selectedTitle.textContent = video.title;
        selectedDiv.classList.remove('d-none');
        selectedDiv.dataset.videoId = video.video_id;

        // Hide results after selection
        resultsDiv.innerHTML = '';
        searchInput.value = '';
    }

    // ─────────────────────────────────────────
    // REMOVE SELECTED VIDEO
    // ─────────────────────────────────────────
    removeBtn.addEventListener('click', function () {
        hiddenVideoId.value = '';
        hiddenTitle.value = '';
        hiddenThumb.value = '';

        selectedDiv.classList.add('d-none');
        selectedThumb.src = '';
        selectedTitle.textContent = '';
    });

    // ─────────────────────────────────────────
    // IMAGE PREVIEW
    // ─────────────────────────────────────────
    const imageInput = document.getElementById('id_image');
    const imagePreview = document.getElementById('imagePreview');

    if (imageInput) {
        imageInput.addEventListener('change', function () {
            imagePreview.innerHTML = '';
            const file = this.files[0];
            if (!file) return;

            if (file.size > 5 * 1024 * 1024) {
                imagePreview.innerHTML = '<div class="alert alert-warning py-2 small">Image too large (max 5MB)</div>';
                this.value = '';
                return;
            }

            const reader = new FileReader();
            reader.onload = function (e) {
                imagePreview.innerHTML = `
                    <img src="${e.target.result}" 
                         style="max-width: 100%; border-radius: 8px; max-height: 300px;">
                `;
            };
            reader.readAsDataURL(file);
        });
    }

    // ─────────────────────────────────────────
    // HELPERS
    // ─────────────────────────────────────────
    function showError(msg) {
        errorDiv.textContent = msg;
        errorDiv.classList.remove('d-none');
        setTimeout(() => errorDiv.classList.add('d-none'), 4000);
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});