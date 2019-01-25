package config

import "time"

const (
	Root = "http://www.zeroorez.net/beauty"
	//Root        = "https://xlui.me"
	PageCount   = 10
	PicSelector = ".post > .text > .post-content > a"
	PicMark     = "[查看原图]"
	Storage     = "./Beauties/"
)

const (
	Interval    = 15 * time.Second
	ChannelSize = 10
	Fetchers    = 1
	Downloaders = 20
	BufSize     = 10 * 1024
)

const (
	Ready = iota
	Success
	Failure
)
