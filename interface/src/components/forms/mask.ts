export const maskDefinitions = {
    '#': { pattern: /\d/ },
    X: { pattern: /[0-9a-zA-Z]/ },
    S: { pattern: /[a-zA-Z]/ },
    A: { pattern: /[a-zA-Z]/, transform: (v: string) => v.toLocaleUpperCase() },
    a: { pattern: /[a-zA-Z]/, transform: (v: string) => v.toLocaleLowerCase() },
    '!': { escape: true }
}

function applyMask(mask: string, value: string) {
    const maskedValue = []
    let unmaskedIndex = 0
    let maskIndex = 0

    while (unmaskedIndex < value.length && maskIndex < mask.length) {
        const maskChar = mask[maskIndex] as '#' | 'X' | 'S' | 'A' | 'a' | '!'
        const unmaskedChar = value[unmaskedIndex]
        const maskDefinition = maskDefinitions[maskChar]

        if (maskDefinition) {
            if ('escape' in maskDefinition && maskDefinition.escape) {
                maskIndex++
                maskedValue.push(value[unmaskedIndex])
                unmaskedIndex++
            } else if ('pattern' in maskDefinition && maskDefinition.pattern.test(unmaskedChar)) {
                const transformedChar =
                    'transform' in maskDefinition && maskDefinition.transform
                        ? maskDefinition.transform(unmaskedChar)
                        : unmaskedChar
                maskedValue.push(transformedChar)
                unmaskedIndex++
            } else {
                break
            }
        } else {
            maskedValue.push(maskChar)
            if (maskChar === unmaskedChar) {
                unmaskedIndex++
            }
        }
        maskIndex++
    }

    return maskedValue.join('')
}

export default applyMask
