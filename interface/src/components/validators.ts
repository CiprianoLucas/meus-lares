import type { Ref } from "vue"

function verifyDate(dateRef: Ref) {
    if (!dateRef.value) {
        return
    }
    let dateString = dateRef.value
    const thisYear = new Date().getFullYear()
    if (dateString.length == 8) {
        const verifyYearSliceString = dateString.slice(-2)
        const verifyYearSlice = Number(verifyYearSliceString)
        dateString = dateString.slice(0, -2)
        const thisYearSlice = thisYear - 2000

        if (verifyYearSlice >= thisYearSlice) {
            dateString += '19' + verifyYearSliceString
        } else {
            dateString += '20' + verifyYearSliceString
        }
        dateRef.value = dateString
    }
    if (dateString.length != 10) {
        return 'Data inválida'
    }

    const dateRegex = /^(\d{2})\/(\d{2})\/(\d{4})$/
    const match = dateString.match(dateRegex)
    if (!match) {
        return 'Data inválida'
    }

    const day = parseInt(match[1], 10)
    const month = parseInt(match[2], 10)
    const year = parseInt(match[3], 10)

    if (year < 1900 || year >= thisYear) {
        return 'Data inválida'
    }

    const date = new Date(year, month - 1, day)

    const is_date =
        date.getFullYear() === year && date.getMonth() === month - 1 && date.getDate() === day

    if (!is_date) return 'Data inválida'
}

function verifyCpf(cpfRef: Ref<string>): string | false {
    let cpf = cpfRef.value
    cpf = cpf.replace(/\D/g, '');
    if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)) {
        return "CPF inválido";
    }
    const digits = cpf.split('').map(Number);
    const calculateDigit = (factor: number) => {
        const sum = digits.slice(0, factor - 1).reduce((acc, num, index) => acc + num * (factor - index), 0);
        return (sum * 10) % 11 % 10;
    };
    const isValid = calculateDigit(10) === digits[9] && calculateDigit(11) === digits[10];
    return isValid?false:"CPF inválido"
}


export {verifyDate, verifyCpf}