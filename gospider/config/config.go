package config

const (
	Root        = "http://www.zeroorez.net/beauty"
	PageCount   = 185
	PicSelector = ".post > .text > .post-content > a"
	PicMark     = "[查看原图]"
	Storage     = "./Beauties/"
)

const (
	ChannelSize = 10
	Fetchers    = 1
	Downloaders = 10
)

const (
	Ready = iota
	Success
	Failure
)
