class Boggle {
    constructor(seconds = 60) {
        this.seconds = seconds;
        setInterval(this.tick.bind(this), 1000)
        this.score = 0;
        this.gameOver = false;
        this.wordsSubmitted = new Set()

        this.wordForm = document.getElementById('add-word');
        this.wordForm.addEventListener('submit', this.handleSubmit);
    }

    tick() {
        let timer = document.getElementById('timer')
        if ((game.gameOver != true)) {
            if (this.seconds === 0) {
                // if the timer is at 0 we end the game
                this.endGame()
            } else {
                this.seconds--;
                timer.innerHTML = this.seconds;
            }
        }
    }

    async handleSubmit(event) {
        event.preventDefault();

        if (game.gameOver) {
            alert('The game is over. Start a new game!')
        } else {
            let word = $("input[name=word]").val();

            if (game.wordsSubmitted.has(word)) {
                alert('This guess has already been submitted')
            } else {
                game.wordsSubmitted.add(word)

                //if input field is empty message player to put in value
                if (word.length <= 0) {
                    alert('Please enter a word')
                    return;
                }

                //send request to server to check word validation
                const res = await axios.get("/check-word", { params: { word: word } });
                if (res.data.result === 'not-word') {
                    alert(`${word} is not a valid English word`);
                } else if (res.data.result === 'not-on-board') {
                    alert(`${word} is not a word on the board`);
                } else {
                    //add the score to our current - points based on length of word
                    game.score += word.length;
                    //grab score HTML ele and update inner HTML with our cur score
                    let currentScore = document.getElementById("current-score");
                    currentScore.innerHTML = game.score;
                }
            }
        }
    }

    async endGame() {
        this.gameOver = true;
        timer.innerHTML = 'Game Over!'
        const res = await axios.post("/post-score", { current_score: game.score });

        let highscore = document.getElementById('highscore')
        let playthroughs = document.getElementById('playthroughs')

        //first index of data returned in the new highscore or current highscore
        //second index of data returned is the times played through
        highscore.innerHTML = res.data[0]
        playthroughs.innerHTML = res.data[1]
    }
}



