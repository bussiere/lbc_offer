package PriceMaster

import (
	"fmt"
	"math"
	"sort"
)

// type
type MeanMedian struct {
	numbers []float64
}
func (mm *MeanMedian) IsOdd() bool {
	if len(mm.numbers)%2 == 0 {
		return false
	}

	return true
}

func (mm *MeanMedian) CalcMedian(n ...float64) float64 {
	sort.Float64s(mm.numbers) // sort the numbers

	mNumber := len(mm.numbers) / 2

	if mm.IsOdd() {
		return mm.numbers[mNumber]
	}

	return (mm.numbers[mNumber-1] + mm.numbers[mNumber]) / 2
}
