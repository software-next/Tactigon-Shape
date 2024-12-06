import sys

from typing import Iterable, Optional, List, Tuple, Any

from click import Option

from ..models import TSpeechObject, HotWord, HotWords, TSpeech

if sys.platform == "win32":
    def walk(args, s: TSpeech, level: int = 0, parent: str = "_init_"):
        if level > len(args) - 1:
            args.append(dict())

        if parent not in args[level]:
            args[level][parent] = list(["---"] if level > 0 else [])

        for hw in s.hotwords:
            if hw.word not in args[level][parent]:
                args[level][parent].append(hw.word)
            if s.children:
                for child in s.children.t_speech:
                    walk(args, child, level + 1, hw.word)

    def get_next_remaining_branch(tree: Optional[List[HotWords]], *levels) -> List[HotWord]:  
        if tree is None:
            return []
        
        if not levels:
            return [branch[0] for branch in tree]
        
        current_level, *rest = levels
        try:
            current_obj = [b[0] for b in tree[current_level][1]]
        except:
            return []
        
        if len(rest) == 0:
            return current_obj
        
        next_tree = tree[current_level][1]

        return (get_next_remaining_branch(next_tree, *rest))

    def get_hotword_from_tree(tree: Optional[List[HotWords]], *levels) -> List[HotWord]:
        if not tree:
            return []
        
        if not levels:
            return [branch[0] for branch in tree]
        
        current_level, *rest = levels
        current_obj = tree[current_level][0]
        
        if len(rest) == 0:
            return [current_obj]
        
        next_tree = tree[current_level][1]

        return [current_obj] + (get_hotword_from_tree(next_tree, *rest))

    def tspeech_combinations(tspeech: Optional[TSpeechObject]) -> Optional[List[HotWords]]:  
        if not tspeech:
            return None
        
        return [(hw, tspeech_combinations(ts.children)) for ts in tspeech.t_speech for hw in ts.hotwords]

else:
    def walk (args, s, level, parent):
        return []
    
    def get_next_remaining_branch(tree, *levels):
        return None
    
    def get_hotword_from_tree(tree, *levels):
        return []
    
    def tspeech_combinations(tspeech: TSpeechObject):
        return []