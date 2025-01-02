const big = 1000
let total_calories = parseFloat(document.getElementById('total_calories').innerHTML)
let total_protein = parseFloat(document.getElementById('total_protein').innerHTML)
let total_fats = parseFloat(document.getElementById('total_fats').innerHTML)
let total_carbs = parseFloat(document.getElementById('total_carbs').innerHTML)
let progress = ((total_calories * 100) / big).toFixed(1)
let total = total_protein + total_fats + total_carbs
let total_proteinP = Math.round((total_protein / total) * 100)
let total_fatsP = Math.round((total_fats / total) * 100)
let total_carbsP = Math.round((total_carbs / total) * 100)
console.log(typeof (total_carbs));
document.getElementById('progress').style.width = `${progress}%`
document.getElementById('progress').innerHTML = `${progress}%`
console.log(total_calories);
console.log(progress);

const ctx = document.getElementById('myChart');
new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Carbs' + total_carbsP + '%', 'Protein' + total_proteinP + '%', 'Fats' + total_fatsP + '%'],
        datasets: [{
            label: '# of Votes',
            data: [total_carbsP, total_proteinP, total_fatsP],
            borderWidth: 1
        }]
    },

});