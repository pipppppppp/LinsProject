async function loadProfit() {

    const periode =
        document.getElementById(
            "periode"
        ).value;

    const startDate =
        document.getElementById(
            "start_date"
        ).value;

    const endDate =
        document.getElementById(
            "end_date"
        ).value;

    try {

        const response =
            await fetch(

                `/report/profit/data?periode=${periode}&start_date=${startDate}&end_date=${endDate}`

            );

        const result =
            await response.json();

        if (!result.status) {

            alert(
                result.message
            );

            return;
        }

        document.getElementById(
            "omset"
        ).innerText =
            formatRupiah(
                result.data.omset
            );

        document.getElementById(
            "laba-barang"
        ).innerText =
            formatRupiah(
                result.data.laba_barang
            );

        document.getElementById(
            "laba-jasa"
        ).innerText =
            formatRupiah(
                result.data.laba_jasa
            );

        document.getElementById(
            "laba-bersih"
        ).innerText =
            formatRupiah(
                result.data.laba_bersih
            );

    } catch (error) {

        console.error(error);

    }
}

function formatRupiah(
    angka
) {

    return "Rp " +
        angka.toLocaleString(
            "id-ID"
        );
}
// loadProfit();

async function loadProfitChart() {

    const response =
        await fetch(
            "/report/profit/chart"
        );

    const result =
        await response.json();

    const bulan =
        result.data.map(
            item => item.bulan
        );
    
    const labaBarang =
        result.data.map(
            item => item.laba_barang
        );
    
    const labaJasa =
        result.data.map(
            item => item.laba_jasa
        );

    const laba =
        result.data.map(
            item => item.laba
        );

    renderChart(
        bulan,
        labaBarang,
        labaJasa,
        laba
    );
}

function renderChart(
    bulan,
    laba,
    laba_barang,
    laba_jasa
){

    const options = {

        chart: {
            type: 'line',
            height: 350
        },

        series: 
        [
            {
                name: 'Laba',
                data: laba
            },
            {
                name: 'Laba Barang',
                data: laba_barang
            },
        
            {
                name: 'Laba Jasa',
                data: laba_jasa
            }
        ],

        xaxis: {
            categories: bulan
        }

    };

    document
        .querySelector(
            "#profit-chart"
        )
        .innerHTML = "";

    new ApexCharts(
        document.querySelector(
            "#profit-chart"
        ),
        options
    ).render();
}

function exportPDF() {

    const periode =
        document.getElementById(
            "periode"
        ).value;

    const startDate =
        document.getElementById(
            "start_date"
        ).value;

    const endDate =
        document.getElementById(
            "end_date"
        ).value;

    window.open(
        `/report/profit/pdf?periode=${periode}&start_date=${startDate}&end_date=${endDate}`,
        "_blank"
    );

    console.log(
        `/report/profit/pdf?periode=${periode}&start_date=${startDate}&end_date=${endDate}`
    );

}

loadProfit();

loadProfitChart();

