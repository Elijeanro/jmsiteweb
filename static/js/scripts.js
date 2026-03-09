// Animation au scroll pour les cartes
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.card');
    const options = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, options);

    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s, transform 0.5s';
        observer.observe(card);
    });
});

// Gestion du carousel personnalisé
document.addEventListener('DOMContentLoaded', function() {
    const carousel = new bootstrap.Carousel(document.getElementById('homeCarousel'), {
        interval: 5000,
        pause: 'hover'
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const boardFilterForm = document.getElementById('boardFilterForm');
    const boardSelect = document.getElementById('boardSelect');
    const decanalBoardsContainer = document.getElementById('decanalBoardsContainer');
    const parishBoardsContainer = document.getElementById('parishBoardsContainer');
    const defaultBoardMembers = document.getElementById('defaultBoardMembers');
    const doyenneSelect = document.getElementById('doyenneSelect');
    const parishSelect = document.getElementById('parishSelect');

    if (boardFilterForm) {
        boardFilterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const boardType = boardSelect.value;

            // Masquer tous les conteneurs
            decanalBoardsContainer.style.display = 'none';
            parishBoardsContainer.style.display = 'none';
            defaultBoardMembers.style.display = 'none';

            // Afficher le bon conteneur
            if (boardType === 'decanal') {
                decanalBoardsContainer.style.display = 'block';
            } else if (boardType === 'parish') {
                parishBoardsContainer.style.display = 'block';
            } else {
                defaultBoardMembers.style.display = 'block';
            }
        });
    }

    // Chargement des membres décanaux
    if (doyenneSelect) {
        doyenneSelect.addEventListener('change', function() {
            const doyenneId = this.value;
            if (doyenneId) {
                fetch(`/get-decanal-members/?doyenne_id=${doyenneId}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            document.getElementById('decanalBoardMembers').innerHTML = data.html;
                        }
                    });
            }
        });
    }

    // Chargement des membres paroissiaux
    if (parishSelect) {
        parishSelect.addEventListener('change', function() {
            const parishId = this.value;
            if (parishId) {
                fetch(`/get-parish-members/?parish_id=${parishId}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            document.getElementById('parishBoardMembers').innerHTML = data.html;
                        }
                    });
            }
        });
    }
});
